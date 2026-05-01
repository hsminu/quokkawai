from enum import Enum
from typing import Generic, List, TypeVar

from pydantic import BaseModel


# 서버/DB에서 쓰는 앱 카테고리 enum
class AppCategory(str, Enum):
    STUDY = "STUDY"
    PRODUCTIVITY = "PRODUCTIVITY"
    COMMUNICATION = "COMMUNICATION"
    ENTERTAINMENT = "ENTERTAINMENT"
    GAME = "GAME"
    SNS = "SNS"
    SYSTEM = "SYSTEM"
    ETC = "ETC"


CATEGORIES = [category.value for category in AppCategory]


# API 에러 응답 내부 구조
class ErrorDetail(BaseModel):
    code: str
    message: str
    detail: str | None = None


# API 에러 응답
class ErrorResponse(BaseModel):
    error: ErrorDetail


# 단순 성공 메시지 응답
class SuccessMessageResponse(BaseModel):
    message: str


T = TypeVar("T")


# 공통 리스트 응답
class ListResponse(BaseModel, Generic[T]):
    items: List[T]
