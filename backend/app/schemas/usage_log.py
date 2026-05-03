from typing import List

from pydantic import BaseModel, Field

from app.schemas.common import AppCategory


# 단일 앱 사용 로그 입력값
class UsageLogCreateItem(BaseModel):
    date: str
    packageName: str
    appName: str
    usageSeconds: int = Field(..., gt=0)
    openCount: int | None = Field(default=None, ge=0)


# Phase 1 개발용: userId를 body로 받는 단일 저장 요청
class UsageLogCreateRequest(UsageLogCreateItem):
    userId: str


# 여러 앱 로그를 한 번에 저장하는 요청
class UsageLogBulkCreateRequest(BaseModel):
    userId: str
    logs: List[UsageLogCreateItem]


# 저장/조회 시 반환되는 사용 로그 형태
class UsageLogResponse(BaseModel):
    usageLogId: str
    userId: str
    date: str
    packageName: str
    appName: str
    category: AppCategory
    usageSeconds: int
    openCount: int | None = None


# 단일 저장 응답
class UsageLogCreateResponse(BaseModel):
    message: str
    usageLog: UsageLogResponse


# 벌크 저장 응답
class UsageLogBulkCreateResponse(BaseModel):
    message: str
    savedCount: int


# 특정 날짜 로그 목록 응답
class UsageLogListResponse(BaseModel):
    date: str
    logs: List[UsageLogResponse]
