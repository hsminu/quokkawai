from fastapi import APIRouter, Query

from app.repositories import usage_log_repository
from app.schemas.usage_log import (
    UsageLogBulkCreateRequest,
    UsageLogBulkCreateResponse,
    UsageLogCreateRequest,
    UsageLogCreateResponse,
    UsageLogListResponse,
)


router = APIRouter(prefix="/usage-logs", tags=["usage-logs"])


# 앱 하나의 하루 사용 로그 저장
@router.post("", response_model=UsageLogCreateResponse)
def create_usage_log(request: UsageLogCreateRequest) -> UsageLogCreateResponse:
    usage_log = usage_log_repository.save(user_id=request.userId, item=request)
    return UsageLogCreateResponse(message="usage log saved", usageLog=usage_log)


# 여러 앱의 하루 사용 로그를 한 번에 저장
@router.post("/bulk", response_model=UsageLogBulkCreateResponse)
def create_usage_logs_bulk(
    request: UsageLogBulkCreateRequest,
) -> UsageLogBulkCreateResponse:
    for log in request.logs:
        usage_log_repository.save(user_id=request.userId, item=log)
    return UsageLogBulkCreateResponse(
        message="usage logs saved",
        savedCount=len(request.logs),
    )


# 특정 날짜의 사용 로그 조회
@router.get("", response_model=UsageLogListResponse)
def list_usage_logs(
    userId: str = Query(...),
    date: str = Query(...),
) -> UsageLogListResponse:
    logs = usage_log_repository.list_by_user_and_date(user_id=userId, date=date)
    return UsageLogListResponse(date=date, logs=logs)
