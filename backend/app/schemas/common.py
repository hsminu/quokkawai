from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


CATEGORIES = [
    "공부",
    "생산성",
    "커뮤니케이션",
    "정보검색",
    "소셜 미디어",
    "엔터테인먼트",
    "게임",
    "기타",
]


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail


class SuccessMessageResponse(BaseModel):
    success: bool = True
    message: str


class ListResponse(BaseModel, Generic[T]):
    success: bool = True
    items: List[T]


class CategoryListResponse(BaseModel):
    success: bool = True
    categories: List[str]
