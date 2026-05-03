from typing import List

from pydantic import BaseModel

from app.schemas.common import AppCategory


# 앱 하나의 카테고리 정보
class AppCategoryResponse(BaseModel):
    packageName: str
    appName: str
    category: AppCategory
    isUserDefined: bool


# 앱 카테고리 목록 응답
class AppCategoryListResponse(BaseModel):
    categories: List[AppCategoryResponse]


# 앱 카테고리 수정 요청
class AppCategoryUpdateRequest(BaseModel):
    appName: str
    category: AppCategory


# 앱 카테고리 수정 응답
class AppCategoryUpdateResponse(BaseModel):
    message: str
    category: AppCategoryResponse
