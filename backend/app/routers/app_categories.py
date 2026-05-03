from fastapi import APIRouter

from app.repositories import app_category_repository
from app.schemas.app_category import (
    AppCategoryListResponse,
    AppCategoryUpdateRequest,
    AppCategoryUpdateResponse,
)


router = APIRouter(prefix="/app-categories", tags=["app-categories"])


# 서버가 알고 있는 앱 카테고리 목록 조회
@router.get("", response_model=AppCategoryListResponse)
def list_app_categories() -> AppCategoryListResponse:
    return AppCategoryListResponse(
        categories=app_category_repository.list_categories(),
    )


# 특정 앱의 카테고리를 사용자 기준으로 수정
@router.put("/{packageName}", response_model=AppCategoryUpdateResponse)
def update_app_category(
    packageName: str,
    request: AppCategoryUpdateRequest,
) -> AppCategoryUpdateResponse:
    category = app_category_repository.upsert_category(
        package_name=packageName,
        request=request,
    )
    return AppCategoryUpdateResponse(
        message="app category updated",
        category=category,
    )
