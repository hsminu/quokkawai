from fastapi import APIRouter, Query

from app.repositories import usage_log_repository
from app.schemas.summary import DailySummaryResponse
from app.services import build_daily_summary


router = APIRouter(prefix="/summary", tags=["summary"])


# 특정 날짜의 전체/앱별/카테고리별 요약 조회
@router.get("/daily", response_model=DailySummaryResponse)
def get_daily_summary(
    userId: str = Query(...),
    date: str = Query(...),
) -> DailySummaryResponse:
    logs = usage_log_repository.list_by_user_and_date(user_id=userId, date=date)
    return build_daily_summary(date=date, logs=logs)
