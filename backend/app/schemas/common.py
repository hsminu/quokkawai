from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel

#########################################
#공통 응답 형식, 에러 형식, 카테고리 목록
########################################


# 제네릭 응답 타입에서 사용할 타입 변수
T = TypeVar("T")


#공통으로 사용할 앱 카테고리 목록
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


# 에러의 세부 정보
class ErrorDetail(BaseModel):
    code: str
    message: str


# 공통 에러 응답 형식
class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail


# 단순 성공 메시지 응답 형식
class SuccessMessageResponse(BaseModel):
    success: bool = True
    message: str


# 리스트 형태 데이터를 반환할 때 사용할 수 있는 공통 응답 형식
class ListResponse(BaseModel, Generic[T]):
    success: bool = True
    items: List[T]


# 카테고리 목록 조회 API 응답 형식
class CategoryListResponse(BaseModel):
    success: bool = True
    categories: List[str]
