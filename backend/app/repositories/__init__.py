from app.config import settings
from app.repositories.in_memory import (
    InMemoryAppCategoryRepository,
    InMemoryUsageLogRepository,
    InMemoryUserSettingsRepository,
)


def _create_repositories():
    if settings.database_backend.lower() == "firestore":
        from app.repositories.firestore import (
            FirestoreAppCategoryRepository,
            FirestoreUsageLogRepository,
            FirestoreUserSettingsRepository,
            create_firestore_client,
        )

        db = create_firestore_client()
        category_repository = FirestoreAppCategoryRepository(db)
        usage_repository = FirestoreUsageLogRepository(db, category_repository)
        settings_repository = FirestoreUserSettingsRepository(db)
        return category_repository, usage_repository, settings_repository

    category_repository = InMemoryAppCategoryRepository()
    usage_repository = InMemoryUsageLogRepository(category_repository)
    settings_repository = InMemoryUserSettingsRepository()
    return category_repository, usage_repository, settings_repository


app_category_repository, usage_log_repository, settings_repository = (
    _create_repositories()
)

__all__ = [
    "app_category_repository",
    "usage_log_repository",
    "settings_repository",
]
