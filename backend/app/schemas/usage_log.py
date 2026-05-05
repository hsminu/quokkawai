from typing import List

from pydantic import BaseModel, Field

from app.schemas.common import AppCategory


class UsageLogCreateItem(BaseModel):
    date: str
    packageName: str
    appName: str
    usageSeconds: int = Field(..., gt=0)
    openCount: int | None = Field(default=None, ge=0)


class UsageLogCreateRequest(UsageLogCreateItem):
    userId: str


class UsageLogBulkCreateRequest(BaseModel):
    userId: str
    logs: List[UsageLogCreateItem]


class UsageLogBulkCreateMeRequest(BaseModel):
    logs: List[UsageLogCreateItem]


class UsageLogResponse(BaseModel):
    usageLogId: str
    userId: str
    date: str
    packageName: str
    appName: str
    category: AppCategory
    usageSeconds: int
    openCount: int | None = None


class UsageLogCreateResponse(BaseModel):
    message: str
    usageLog: UsageLogResponse


class UsageLogBulkCreateResponse(BaseModel):
    message: str
    savedCount: int


class UsageLogListResponse(BaseModel):
    date: str
    logs: List[UsageLogResponse]
