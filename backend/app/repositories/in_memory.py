from app.schemas.app_category import AppCategoryResponse, AppCategoryUpdateRequest
from app.schemas.common import AppCategory
from app.schemas.usage_log import UsageLogCreateItem, UsageLogResponse
from app.services.openai_category_service import classify_app_category


# Known app categories used before asking AI.
DEFAULT_APP_CATEGORIES = [
    AppCategoryResponse(
        packageName="com.google.android.youtube",
        appName="YouTube",
        category=AppCategory.ENTERTAINMENT,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.instagram.android",
        appName="Instagram",
        category=AppCategory.SNS,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.nhn.android.webtoon",
        appName="Naver Webtoon",
        category=AppCategory.ENTERTAINMENT,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.kakao.talk",
        appName="KakaoTalk",
        category=AppCategory.COMMUNICATION,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.google.android.gm",
        appName="Gmail",
        category=AppCategory.COMMUNICATION,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.google.android.calendar",
        appName="Google Calendar",
        category=AppCategory.PRODUCTIVITY,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.android.settings",
        appName="Settings",
        category=AppCategory.SYSTEM,
        isUserDefined=False,
    ),
]


# Packages matching these prefixes are classified locally as system apps.
SYSTEM_PACKAGE_PREFIXES = (
    "com.android.",
    "com.google.android.gms",
    "com.google.android.inputmethod",
    "com.samsung.android.app.launcher",
)


class InMemoryAppCategoryRepository:
    def __init__(self) -> None:
        self._categories = {
            category.packageName: category for category in DEFAULT_APP_CATEGORIES
        }

    def list_categories(self) -> list[AppCategoryResponse]:
        # Keep responses stable for easier testing.
        return sorted(self._categories.values(), key=lambda item: item.packageName)

    def get_category(self, package_name: str, app_name: str) -> AppCategoryResponse:
        # User-defined/default mapping wins.
        if package_name in self._categories:
            return self._categories[package_name]

        # System app rules are cheap and deterministic, so do them before AI.
        if package_name.startswith(SYSTEM_PACKAGE_PREFIXES):
            category = self._build_category(
                package_name=package_name,
                app_name=app_name,
                category=AppCategory.SYSTEM,
                is_user_defined=False,
            )
            self._categories[package_name] = category
            return category

        # Unknown normal apps are classified by AI once, then cached.
        ai_category = classify_app_category(
            package_name=package_name,
            app_name=app_name,
        )
        category = self._build_category(
            package_name=package_name,
            app_name=app_name,
            category=ai_category or AppCategory.ETC,
            is_user_defined=False,
        )
        self._categories[package_name] = category
        return category

    def upsert_category(
        self, package_name: str, request: AppCategoryUpdateRequest
    ) -> AppCategoryResponse:
        # Manual edits override future AI/default classification.
        category = self._build_category(
            package_name=package_name,
            app_name=request.appName,
            category=request.category,
            is_user_defined=True,
        )
        self._categories[package_name] = category
        return category

    def _build_category(
        self,
        package_name: str,
        app_name: str,
        category: AppCategory,
        is_user_defined: bool,
    ) -> AppCategoryResponse:
        return AppCategoryResponse(
            packageName=package_name,
            appName=app_name,
            category=category,
            isUserDefined=is_user_defined,
        )


class InMemoryUsageLogRepository:
    def __init__(self, category_repository: InMemoryAppCategoryRepository) -> None:
        self._category_repository = category_repository
        self._usage_logs: dict[str, UsageLogResponse] = {}

    def save(self, user_id: str, item: UsageLogCreateItem) -> UsageLogResponse:
        # Add a server-side category before saving the usage log.
        category = self._category_repository.get_category(
            package_name=item.packageName,
            app_name=item.appName,
        )
        # Same user/date/app overwrites the previous daily summary row.
        usage_log_id = f"{user_id}_{item.date}_{item.packageName}"
        usage_log = UsageLogResponse(
            usageLogId=usage_log_id,
            userId=user_id,
            date=item.date,
            packageName=item.packageName,
            appName=item.appName,
            category=category.category,
            usageSeconds=item.usageSeconds,
            openCount=item.openCount,
        )
        self._usage_logs[usage_log_id] = usage_log
        return usage_log

    def list_by_user_and_date(self, user_id: str, date: str) -> list[UsageLogResponse]:
        # Return one user's logs for one date, longest usage first.
        logs = [
            log
            for log in self._usage_logs.values()
            if log.userId == user_id and log.date == date
        ]
        return sorted(logs, key=lambda item: item.usageSeconds, reverse=True)


# Shared in-memory repositories used by routers.
app_category_repository = InMemoryAppCategoryRepository()
usage_log_repository = InMemoryUsageLogRepository(app_category_repository)
