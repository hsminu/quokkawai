from pathlib import Path
from typing import Any

from app.config import settings
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


class FirestoreClientError(RuntimeError):
    pass


def create_firestore_client() -> Any:
    # Firebase Admin SDK로 Firestore 클라이언트를 만든다.
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError as exc:
        raise FirestoreClientError(
            "Firestore를 사용하려면 firebase-admin 패키지가 필요합니다."
        ) from exc

    # Admin 앱은 프로세스당 한 번만 초기화해야 한다.
    if not firebase_admin._apps:
        options = {}
        if settings.firebase_project_id:
            options["projectId"] = settings.firebase_project_id

        if settings.firebase_credentials_path:
            credential_path = Path(settings.firebase_credentials_path)
            cred = credentials.Certificate(str(credential_path))
            firebase_admin.initialize_app(cred, options or None)
        else:
            firebase_admin.initialize_app(options=options or None)

    return firestore.client()


class FirestoreAppCategoryRepository:
    def __init__(self, db: Any) -> None:
        self._collection = db.collection("app_categories")
        self._default_categories = {
            category.packageName: category for category in DEFAULT_APP_CATEGORIES
        }

    def list_categories(self) -> list[AppCategoryResponse]:
        # 저장된 카테고리가 없으면 기본 매핑을 보여준다.
        categories = [
            self._from_document(snapshot.to_dict())
            for snapshot in self._collection.stream()
            if snapshot.to_dict()
        ]
        if categories:
            return sorted(categories, key=lambda item: item.packageName)
        return sorted(self._default_categories.values(), key=lambda item: item.packageName)

    def get_category(self, package_name: str, app_name: str) -> AppCategoryResponse:
        # 1순위: Firestore에 저장된 카테고리 캐시
        snapshot = self._collection.document(package_name).get()
        if snapshot.exists:
            return self._from_document(snapshot.to_dict())

        # 2순위: 서버 기본 앱 매핑
        if package_name in self._default_categories:
            category = self._default_categories[package_name]
            self._save_category(category)
            return category

        # 3순위: 시스템 앱 prefix 규칙
        if package_name.startswith(SYSTEM_PACKAGE_PREFIXES):
            category = self._build_category(
                package_name=package_name,
                app_name=app_name,
                category=AppCategory.SYSTEM,
                is_user_defined=False,
            )
            self._save_category(category)
            return category

        # 4순위: 모르는 일반 앱은 AI로 분류하고 실패 시 ETC로 저장
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
        self._save_category(category)
        return category

    def upsert_category(
        self, package_name: str, request: AppCategoryUpdateRequest
    ) -> AppCategoryResponse:
        # 사용자가 직접 수정한 카테고리는 항상 우선한다.
        category = self._build_category(
            package_name=package_name,
            app_name=request.appName,
            category=request.category,
            is_user_defined=True,
        )
        self._save_category(category)
        return category

    def _save_category(self, category: AppCategoryResponse) -> None:
        # packageName을 문서 ID로 사용해서 같은 앱은 덮어쓴다.
        document = self._collection.document(category.packageName)
        snapshot = document.get()
        data = {
            **category.model_dump(mode="json"),
            "updatedAt": _server_timestamp(),
        }
        if not snapshot.exists:
            data["createdAt"] = _server_timestamp()
        document.set(data, merge=True)

    def _from_document(self, data: dict[str, Any] | None) -> AppCategoryResponse:
        # Firestore 문서를 API 응답 스키마로 변환한다.
        if not data:
            raise FirestoreClientError("빈 앱 카테고리 문서는 사용할 수 없습니다.")
        return AppCategoryResponse(
            packageName=data["packageName"],
            appName=data["appName"],
            category=AppCategory(data["category"]),
            isUserDefined=bool(data["isUserDefined"]),
        )

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


class FirestoreUsageLogRepository:
    def __init__(
        self,
        db: Any,
        category_repository: FirestoreAppCategoryRepository,
    ) -> None:
        self._collection = db.collection("usage_logs")
        self._category_repository = category_repository

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

        # userId + date + packageName 기준 하루 요약 로그를 저장한다.
        document = self._collection.document(usage_log_id)
        snapshot = document.get()
        data = {
            **usage_log.model_dump(mode="json"),
            "updatedAt": _server_timestamp(),
        }
        if not snapshot.exists:
            data["createdAt"] = _server_timestamp()
        document.set(data, merge=True)
        return usage_log

    def list_by_user_and_date(self, user_id: str, date: str, end_date: str | None = None) -> list[UsageLogResponse]:
        # 특정 사용자의 특정 날짜(혹은 기간) 로그를 조회한다.
        target_end = end_date or date
        snapshots = (
            self._collection.where("userId", "==", user_id)
            .where("date", ">=", date)
            .where("date", "<=", target_end)
            .stream()
        )
        logs = [
            self._from_document(snapshot.to_dict())
            for snapshot in snapshots
            if snapshot.to_dict()
        ]
        if end_date:
            return sorted(logs, key=lambda item: item.date)
        return sorted(logs, key=lambda item: item.usageSeconds, reverse=True)

    def _from_document(self, data: dict[str, Any] | None) -> UsageLogResponse:
        # Firestore 문서를 사용 로그 응답 스키마로 변환한다.
        if not data:
            raise FirestoreClientError("빈 사용 로그 문서는 사용할 수 없습니다.")
        return UsageLogResponse(
            usageLogId=data["usageLogId"],
            userId=data["userId"],
            date=data["date"],
            packageName=data["packageName"],
            appName=data["appName"],
            category=AppCategory(data["category"]),
            usageSeconds=int(data["usageSeconds"]),
            openCount=data.get("openCount"),
        )


class FirestoreUserSettingsRepository:
    def __init__(self, db: Any) -> None:
        self._collection = db.collection("user_settings")

    def get_by_user_id(self, user_id: str) -> UserSettings:
        snapshot = self._collection.document(user_id).get()
        if not snapshot.exists:
            settings = _build_default_settings(user_id)
            self._save(settings)
            return settings

        data = snapshot.to_dict()
        if not data:
            settings = _build_default_settings(user_id)
            self._save(settings)
            return settings

        return self._from_document(data)

    def save(self, user_id: str, request: UserSettingsUpdateRequest) -> UserSettings:
        settings = UserSettings(
            userId=user_id,
            dailyUsageGoalMinutes=request.dailyUsageGoalMinutes,
            targetCategories=request.targetCategories,
            analysisSchedules=request.analysisSchedules,
            analysisTone=request.analysisTone,
            updatedAt=_now_iso(),
        )
        self._save(settings)
        return settings

    def _save(self, settings: UserSettings) -> None:
        data = settings.model_dump(mode="json")
        self._collection.document(settings.userId).set(data, merge=True)

    def _from_document(self, data: dict[str, Any]) -> UserSettings:
        return UserSettings(
            userId=data["userId"],
            dailyUsageGoalMinutes=int(data["dailyUsageGoalMinutes"]),
            targetCategories=data.get("targetCategories") or default_target_categories(),
            analysisSchedules=data.get("analysisSchedules") or [],
            analysisTone=data.get("analysisTone") or "SOFT",
            updatedAt=data["updatedAt"],
        )


class FirestoreUserRepository:
    def __init__(self, db: Any) -> None:
        self._collection = db.collection("users")

    def upsert_google_user(
        self,
        provider_user_id: str,
        email: str | None,
        nickname: str | None,
    ) -> UserResponse:
        user = UserResponse(
            userId=_build_google_user_id(provider_user_id),
            provider="google",
            providerUserId=provider_user_id,
            email=email,
            nickname=nickname,
        )
        document = self._collection.document(user.userId)
        snapshot = document.get()
        data = {
            **user.model_dump(mode="json"),
            "updatedAt": _server_timestamp(),
        }
        if not snapshot.exists:
            data["createdAt"] = _server_timestamp()
        document.set(data, merge=True)
        return user

    def get_by_user_id(self, user_id: str) -> UserResponse | None:
        snapshot = self._collection.document(user_id).get()
        if not snapshot.exists:
            return None
        data = snapshot.to_dict()
        if not data:
            return None
        return UserResponse(
            userId=data["userId"],
            provider=data["provider"],
            providerUserId=data["providerUserId"],
            email=data.get("email"),
            nickname=data.get("nickname"),
        )


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


def _server_timestamp() -> Any:
    # Firestore 서버 시간을 createdAt/updatedAt에 사용한다.
    from firebase_admin import firestore

    return firestore.SERVER_TIMESTAMP
