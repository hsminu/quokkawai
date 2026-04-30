from typing import List
from pydantic import BaseModel


class UsageLogBase(BaseModel):
    date: str
    appName: str
    packageName: str
    category: str | None = None
    minutesUsed: int
    openCount: int | None = None
    notificationCount: int | None = None
    timeOfDay: str | None = None


class UsageLogCreateRequest(UsageLogBase):
    userId: str


class UsageLog(UsageLogBase):
    logId: str
    userId: str
    createdAt: str


class UsageLogResponse(BaseModel):
    success: bool = True
    message: str
    log: UsageLog


class UsageLogBulkCreateRequest(BaseModel):
    userId: str
    logs: List[UsageLogBase]


class UsageLogBulkCreateResponse(BaseModel):
    success: bool = True
    message: str
    savedCount: int


class DailyUsageLogsResponse(BaseModel):
    success: bool = True
    userId: str
    date: str
    logs: List[UsageLog]
