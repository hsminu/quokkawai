from fastapi import APIRouter

from app.repositories import usage_log_repository
from app.schemas.analysis import DailyAnalysisRequest, DailyAnalysisResponse
from app.services import build_daily_analysis, build_daily_summary


router = APIRouter(prefix="/analysis", tags=["analysis"])


# 특정 날짜의 요약 데이터를 기반으로 간단 분석 생성
@router.post("/daily", response_model=DailyAnalysisResponse)
def create_daily_analysis(request: DailyAnalysisRequest) -> DailyAnalysisResponse:
    logs = usage_log_repository.list_by_user_and_date(
        user_id=request.userId,
        date=request.date,
    )
    summary = build_daily_summary(date=request.date, logs=logs)
    return build_daily_analysis(summary)
