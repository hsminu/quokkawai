from app.repositories.defaults import (
    DEFAULT_APP_CATEGORIES,
    SYSTEM_PACKAGE_PREFIXES,
    build_usage_log_id,
)
from app.schemas.app_category import AppCategoryResponse, AppCategoryUpdateRequest
from app.schemas.common import AppCategory
from app.schemas.settings import UserSettings, UserSettingsUpdateRequest, default_target_categories
from app.schemas.usage_log import UsageLogCreateItem, UsageLogResponse
from app.schemas.user import UserResponse
from app.services.openai_category_service import classify_app_category


class InMemoryAppCategoryRepository:
    def __init__(self) -> None:
        # packageName으로 바로 찾을 수 있게 dict로 보관한다.
        self._categories = {
            category.packageName: category for category in DEFAULT_APP_CATEGORIES
        }

    def list_categories(self) -> list[AppCategoryResponse]:
        # 응답 순서를 고정해서 테스트하기 쉽게 한다.
        return sorted(self._categories.values(), key=lambda item: item.packageName)

    def get_category(self, package_name: str, app_name: str) -> AppCategoryResponse:
        # 이미 저장된 카테고리가 있으면 그 값을 사용한다.
        if package_name in self._categories:
            return self._categories[package_name]

        # 시스템 앱은 AI 호출 없이 바로 SYSTEM으로 분류한다.
        if package_name.startswith(SYSTEM_PACKAGE_PREFIXES):
            category = self._build_category(
                package_name=package_name,
                app_name=app_name,
                category=AppCategory.SYSTEM,
                is_user_defined=False,
            )
            self._categories[package_name] = category
            return category

        # 모르는 일반 앱은 AI로 한 번 분류하고 결과를 캐싱한다.
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
        # 사용자가 직접 수정한 카테고리를 저장한다.
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
        # 저장 전에 서버 기준 카테고리를 붙인다.
        category = self._category_repository.get_category(
            package_name=item.packageName,
            app_name=item.appName,
        )
        usage_log_id = build_usage_log_id(
            user_id=user_id,
            date=item.date,
            package_name=item.packageName,
        )
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

    def list_by_user_and_date(self, user_id: str, date: str, end_date: str | None = None) -> list[UsageLogResponse]:
        # 특정 사용자/날짜(혹은 기간) 로그를 골라 반환한다.
        target_end = end_date or date
        logs = [
            log
            for log in self._usage_logs.values()
            if log.userId == user_id and date <= log.date <= target_end
        ]
        if end_date:
            return sorted(logs, key=lambda item: item.date)
        return sorted(logs, key=lambda item: item.usageSeconds, reverse=True)


class InMemoryUserSettingsRepository:
    def __init__(self) -> None:
        self._settings: dict[str, UserSettings] = {}

    def get_by_user_id(self, user_id: str) -> UserSettings:
        if user_id not in self._settings:
            self._settings[user_id] = _build_default_settings(user_id)
        return self._settings[user_id]

    def save(self, user_id: str, request: UserSettingsUpdateRequest) -> UserSettings:
        settings = UserSettings(
            userId=user_id,
            dailyUsageGoalMinutes=request.dailyUsageGoalMinutes,
            targetCategories=request.targetCategories,
            analysisSchedules=request.analysisSchedules,
            analysisTone=request.analysisTone,
            updatedAt=_now_iso(),
        )
        self._settings[user_id] = settings
        return settings


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[str, UserResponse] = {}

    def upsert_google_user(
        self,
        provider_user_id: str,
        email: str | None,
        nickname: str | None,
    ) -> UserResponse:
        user_id = _build_google_user_id(provider_user_id)
        user = UserResponse(
            userId=user_id,
            provider="google",
            providerUserId=provider_user_id,
            email=email,
            nickname=nickname,
        )
        self._users[user_id] = user
        return user


def _build_google_user_id(provider_user_id: str) -> str:
    return f"google_{provider_user_id}"


def _build_default_settings(user_id: str) -> UserSettings:
    return UserSettings(
        userId=user_id,
        dailyUsageGoalMinutes=240,
        targetCategories=default_target_categories(),
        analysisSchedules=[],
        analysisTone="SOFT",
        updatedAt=_now_iso(),
    )


def _now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()
