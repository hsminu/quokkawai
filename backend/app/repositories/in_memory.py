from app.schemas.app_category import AppCategoryResponse, AppCategoryUpdateRequest
from app.schemas.common import AppCategory
from app.schemas.usage_log import UsageLogCreateItem, UsageLogResponse


# 기본으로 알고 있는 앱별 카테고리 목록
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


# 시스템 앱으로 대충 분류할 패키지 prefix
SYSTEM_PACKAGE_PREFIXES = (
    "com.android.",
    "com.google.android.gms",
    "com.google.android.inputmethod",
    "com.samsung.android.app.launcher",
)


# Firestore 붙이기 전 임시 앱 카테고리 저장소
class InMemoryAppCategoryRepository:
    def __init__(self) -> None:
        self._categories = {
            category.packageName: category for category in DEFAULT_APP_CATEGORIES
        }

    def list_categories(self) -> list[AppCategoryResponse]:
        # 패키지명 순서로 고정해서 응답을 예측 가능하게 함
        return sorted(self._categories.values(), key=lambda item: item.packageName)

    def get_category(self, package_name: str, app_name: str) -> AppCategoryResponse:
        # 등록된 앱이면 저장된 카테고리를 그대로 사용
        if package_name in self._categories:
            return self._categories[package_name]

        # 모르는 앱은 시스템 앱이면 SYSTEM, 아니면 ETC
        category = (
            AppCategory.SYSTEM
            if package_name.startswith(SYSTEM_PACKAGE_PREFIXES)
            else AppCategory.ETC
        )
        return AppCategoryResponse(
            packageName=package_name,
            appName=app_name,
            category=category,
            isUserDefined=False,
        )

    def upsert_category(
        self, package_name: str, request: AppCategoryUpdateRequest
    ) -> AppCategoryResponse:
        # 사용자가 직접 수정한 카테고리로 저장
        category = AppCategoryResponse(
            packageName=package_name,
            appName=request.appName,
            category=request.category,
            isUserDefined=True,
        )
        self._categories[package_name] = category
        return category


# Firestore 붙이기 전 임시 사용 로그 저장소
class InMemoryUsageLogRepository:
    def __init__(self, category_repository: InMemoryAppCategoryRepository) -> None:
        self._category_repository = category_repository
        self._usage_logs: dict[str, UsageLogResponse] = {}

    def save(self, user_id: str, item: UsageLogCreateItem) -> UsageLogResponse:
        # 클라이언트가 보낸 로그에 서버 기준 카테고리를 붙임
        category = self._category_repository.get_category(
            package_name=item.packageName,
            app_name=item.appName,
        )
        # 같은 유저/날짜/앱은 하나의 문서처럼 덮어씀
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
        # 특정 유저의 특정 날짜 로그만 골라서 사용 시간 순으로 반환
        logs = [
            log
            for log in self._usage_logs.values()
            if log.userId == user_id and log.date == date
        ]
        return sorted(logs, key=lambda item: item.usageSeconds, reverse=True)


# 앱 전체에서 공유하는 임시 저장소 인스턴스
app_category_repository = InMemoryAppCategoryRepository()
usage_log_repository = InMemoryUsageLogRepository(app_category_repository)
