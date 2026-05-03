from app.schemas.app_category import AppCategoryResponse, AppCategoryUpdateRequest
from app.schemas.common import AppCategory
from app.schemas.usage_log import UsageLogCreateItem, UsageLogResponse
from app.services.openai_category_service import classify_app_category


# AI에 묻기 전에 먼저 사용하는 기본 앱 카테고리 목록
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


# 이 prefix에 맞는 패키지는 로컬에서 시스템 앱으로 분류
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
        # 테스트하기 쉽게 항상 같은 순서로 반환
        return sorted(self._categories.values(), key=lambda item: item.packageName)

    def get_category(self, package_name: str, app_name: str) -> AppCategoryResponse:
        # 사용자 수정값이나 기본 매핑이 있으면 그 값을 우선 사용
        if package_name in self._categories:
            return self._categories[package_name]

        # 시스템 앱 규칙은 빠르고 고정적이므로 AI보다 먼저 처리
        if package_name.startswith(SYSTEM_PACKAGE_PREFIXES):
            category = self._build_category(
                package_name=package_name,
                app_name=app_name,
                category=AppCategory.SYSTEM,
                is_user_defined=False,
            )
            self._categories[package_name] = category
            return category

        # 모르는 일반 앱은 AI로 한 번 분류하고 결과를 캐싱
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
        # 사용자가 직접 수정한 값은 이후 AI/기본 분류보다 우선
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
        # 사용 로그 저장 전에 서버 기준 카테고리를 붙임
        category = self._category_repository.get_category(
            package_name=item.packageName,
            app_name=item.appName,
        )
        # 같은 사용자/날짜/앱은 기존 하루 요약 로그를 덮어씀
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
        # 특정 사용자의 특정 날짜 로그를 사용 시간 긴 순서로 반환
        logs = [
            log
            for log in self._usage_logs.values()
            if log.userId == user_id and log.date == date
        ]
        return sorted(logs, key=lambda item: item.usageSeconds, reverse=True)


# 라우터에서 공유해서 쓰는 인메모리 저장소 인스턴스
app_category_repository = InMemoryAppCategoryRepository()
usage_log_repository = InMemoryUsageLogRepository(app_category_repository)
