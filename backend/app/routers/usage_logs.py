from fastapi import APIRouter, Depends, Query

from app.dependencies import get_current_user
from app.repositories import usage_log_repository
from app.schemas.usage_log import (
    UsageLogBulkCreateMeRequest,
    UsageLogBulkCreateRequest,
    UsageLogBulkCreateResponse,
    UsageLogCreateItem,
    UsageLogCreateRequest,
    UsageLogCreateResponse,
    UsageLogListResponse,
)
from app.schemas.user import UserResponse


router = APIRouter(prefix="/usage-logs", tags=["usage-logs"])


@router.post("/me", response_model=UsageLogCreateResponse)
def create_my_usage_log(
    request: UsageLogCreateItem,
    current_user: UserResponse = Depends(get_current_user),
) -> UsageLogCreateResponse:
    usage_log = usage_log_repository.save(user_id=current_user.userId, item=request)
    return UsageLogCreateResponse(message="usage log saved", usageLog=usage_log)


@router.post("/me/bulk", response_model=UsageLogBulkCreateResponse)
def create_my_usage_logs_bulk(
    request: UsageLogBulkCreateMeRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> UsageLogBulkCreateResponse:
    for log in request.logs:
        usage_log_repository.save(user_id=current_user.userId, item=log)
    return UsageLogBulkCreateResponse(
        message="usage logs saved",
        savedCount=len(request.logs),
    )


@router.get("/me", response_model=UsageLogListResponse)
def list_my_usage_logs(
    date: str = Query(...),
    current_user: UserResponse = Depends(get_current_user),
) -> UsageLogListResponse:
    logs = usage_log_repository.list_by_user_and_date(
        user_id=current_user.userId,
        date=date,
    )
    return UsageLogListResponse(date=date, logs=logs)


@router.post("", response_model=UsageLogCreateResponse)
def create_usage_log(request: UsageLogCreateRequest) -> UsageLogCreateResponse:
    usage_log = usage_log_repository.save(user_id=request.userId, item=request)
    return UsageLogCreateResponse(message="usage log saved", usageLog=usage_log)


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


@router.get("", response_model=UsageLogListResponse)
def list_usage_logs(
    userId: str = Query(...),
    date: str = Query(...),
) -> UsageLogListResponse:
    logs = usage_log_repository.list_by_user_and_date(user_id=userId, date=date)
    return UsageLogListResponse(date=date, logs=logs)
