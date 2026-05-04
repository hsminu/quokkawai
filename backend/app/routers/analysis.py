from fastapi import APIRouter

from app.repositories import usage_log_repository
from app.schemas.analysis import DailyAnalysisRequest, DailyAnalysisResponse
from app.schemas.report import AICoachingReportCreateRequest, AICoachingReportCreateResponse
from app.services import build_daily_analysis, build_daily_summary, build_weekly_analysis


router = APIRouter(prefix="/analysis", tags=["analysis"])


# 특정 날짜의 요약 데이터를 기반으로 간단 분석 생성
@router.post("/daily", response_model=DailyAnalysisResponse)
def create_daily_analysis(request: DailyAnalysisRequest) -> DailyAnalysisResponse:
    logs = usage_log_repository.list_by_user_and_date(
        user_id=request.userId,
        date=request.date,
    )
    summary = build_daily_summary(date=request.date, logs=logs)
    return build_daily_analysis(summary, request.coachTone)

@router.post("/weekly", response_model=AICoachingReportCreateResponse)
def create_weekly_analysis(request: AICoachingReportCreateRequest) -> AICoachingReportCreateResponse:
    # 1. startDate와 endDate를 기반으로 주간 데이터를 가져옵니다.
    logs = usage_log_repository.list_by_user_and_date(
        user_id=request.userId,
        date=request.startDate,
        end_date=request.endDate,
    )
    # 2. 가져온 데이터를 바탕으로 주간 리포트를 생성합니다.
    return build_weekly_analysis(request=request, logs=logs)
