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
from app.schemas.usage_log import UsageLogCreateItem, UsageLogResponse
from app.services.openai_category_service import classify_app_category


class FirestoreClientError(RuntimeError):
    pass


def create_firestore_client() -> Any:
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError as exc:
        raise FirestoreClientError(
            "Firestore를 사용하려면 firebase-admin 패키지가 필요합니다."
        ) from exc

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
        self._db = db
        self._collection = db.collection("app_categories")
        self._default_categories = {
            category.packageName: category for category in DEFAULT_APP_CATEGORIES
        }

    def list_categories(self) -> list[AppCategoryResponse]:
        categories = [
            self._from_document(snapshot.to_dict())
            for snapshot in self._collection.stream()
            if snapshot.to_dict()
        ]
        if categories:
            return sorted(categories, key=lambda item: item.packageName)
        return sorted(self._default_categories.values(), key=lambda item: item.packageName)

    def get_category(self, package_name: str, app_name: str) -> AppCategoryResponse:
        snapshot = self._collection.document(package_name).get()
        if snapshot.exists:
            return self._from_document(snapshot.to_dict())

        if package_name in self._default_categories:
            category = self._default_categories[package_name]
            self._save_category(category)
            return category

        if package_name.startswith(SYSTEM_PACKAGE_PREFIXES):
            category = self._build_category(
                package_name=package_name,
                app_name=app_name,
                category=AppCategory.SYSTEM,
                is_user_defined=False,
            )
            self._save_category(category)
            return category

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
        category = self._build_category(
            package_name=package_name,
            app_name=request.appName,
            category=request.category,
            is_user_defined=True,
        )
        self._save_category(category)
        return category

    def _save_category(self, category: AppCategoryResponse) -> None:
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

    def list_by_user_and_date(self, user_id: str, date: str) -> list[UsageLogResponse]:
        snapshots = (
            self._collection.where("userId", "==", user_id)
            .where("date", "==", date)
            .stream()
        )
        logs = [
            self._from_document(snapshot.to_dict())
            for snapshot in snapshots
            if snapshot.to_dict()
        ]
        return sorted(logs, key=lambda item: item.usageSeconds, reverse=True)

    def _from_document(self, data: dict[str, Any] | None) -> UsageLogResponse:
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


def _server_timestamp() -> Any:
    from firebase_admin import firestore

    return firestore.SERVER_TIMESTAMP
