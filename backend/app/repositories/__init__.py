from app.config import settings
from app.repositories.in_memory import (
    InMemoryAppCategoryRepository,
    InMemoryUsageLogRepository,
)


def _create_repositories():
    # .env 설정에 따라 실제 저장소 구현을 선택한다.
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

    # 기본값은 로컬 개발용 인메모리 저장소다.
    category_repository = InMemoryAppCategoryRepository()
    usage_repository = InMemoryUsageLogRepository(category_repository)
    return category_repository, usage_repository


# 라우터가 공통으로 사용하는 저장소 인스턴스
app_category_repository, usage_log_repository = _create_repositories()

__all__ = ["app_category_repository", "usage_log_repository"]
