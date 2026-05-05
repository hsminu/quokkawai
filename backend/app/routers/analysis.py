from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.repositories import settings_repository, usage_log_repository
from app.schemas.analysis import (
    DailyAnalysisMeRequest,
    DailyAnalysisRequest,
    DailyAnalysisResponse,
)
from app.schemas.report import AICoachingReportCreateRequest, AICoachingReportCreateResponse
from app.schemas.user import UserResponse
from app.services import build_daily_analysis, build_daily_summary, build_weekly_analysis


router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/daily/me", response_model=DailyAnalysisResponse)
def create_my_daily_analysis(
    request: DailyAnalysisMeRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> DailyAnalysisResponse:
    logs = usage_log_repository.list_by_user_and_date(
        user_id=current_user.userId,
        date=request.date,
    )
    summary = build_daily_summary(date=request.date, logs=logs)
    user_settings = settings_repository.get_by_user_id(current_user.userId)
    return build_daily_analysis(summary, user_settings=user_settings)


@router.post("/daily", response_model=DailyAnalysisResponse)
def create_daily_analysis(request: DailyAnalysisRequest) -> DailyAnalysisResponse:
    logs = usage_log_repository.list_by_user_and_date(
        user_id=request.userId,
        date=request.date,
    )
    summary = build_daily_summary(date=request.date, logs=logs)
    user_settings = settings_repository.get_by_user_id(request.userId)
    return build_daily_analysis(summary, user_settings=user_settings)


@router.post("/weekly", response_model=AICoachingReportCreateResponse)
def create_weekly_analysis(
    request: AICoachingReportCreateRequest,
) -> AICoachingReportCreateResponse:
    logs = usage_log_repository.list_by_user_and_date(
        user_id=request.userId,
        date=request.startDate,
        end_date=request.endDate,
    )
    user_settings = settings_repository.get_by_user_id(request.userId)
    return build_weekly_analysis(
        request=request,
        logs=logs,
        user_settings=user_settings,
    )
