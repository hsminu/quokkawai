from app.config import settings
from app.repositories.in_memory import (
    InMemoryAppCategoryRepository,
    InMemoryUsageLogRepository,
)


def _create_repositories():
    if settings.database_backend.lower() == "firestore":
        from app.repositories.firestore import (
            FirestoreAppCategoryRepository,
            FirestoreUsageLogRepository,
            create_firestore_client,
        )

        db = create_firestore_client()
        category_repository = FirestoreAppCategoryRepository(db)
        usage_repository = FirestoreUsageLogRepository(db, category_repository)
        return category_repository, usage_repository

    category_repository = InMemoryAppCategoryRepository()
    usage_repository = InMemoryUsageLogRepository(category_repository)
    return category_repository, usage_repository


app_category_repository, usage_log_repository = _create_repositories()

__all__ = ["app_category_repository", "usage_log_repository"]
