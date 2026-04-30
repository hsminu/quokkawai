from typing import List
from pydantic import BaseModel


###############################
# Android 사용 로그 데이터 타입
###############################



# 앱 사용 로그의 공통 필드
# 단일 업로드와 대량 업로드에서 공통으로 사용한다.
class UsageLogBase(BaseModel):
    date: str
    appName: str
    packageName: str
    category: str | None = None
    minutesUsed: int
    openCount: int | None = None
    notificationCount: int | None = None
    timeOfDay: str | None = None


# 사용 로그 단일 업로드 요청
class UsageLogCreateRequest(UsageLogBase):
    userId: str


# 서버에 저장된 사용 로그 최종 형태
class UsageLog(UsageLogBase):
    logId: str
    userId: str
    createdAt: str


# 사용 로그 단일 업로드 응답
class UsageLogResponse(BaseModel):
    success: bool = True
    message: str
    log: UsageLog


# 사용 로그 대량 업로드 요청
# Android에서 하루치 로그를 한 번에 보낼 때 사용한다.
class UsageLogBulkCreateRequest(BaseModel):
    userId: str
    logs: List[UsageLogBase]


# 사용 로그 대량 업로드 응답
class UsageLogBulkCreateResponse(BaseModel):
    success: bool = True
    message: str
    savedCount: int


# 특정 날짜의 사용 로그 조회 응답
class DailyUsageLogsResponse(BaseModel):
    success: bool = True
    userId: str
    date: str
    logs: List[UsageLog]
