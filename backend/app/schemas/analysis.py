from typing import List

from pydantic import BaseModel

from app.schemas.common import AppCategory
from app.schemas.summary import TopAppUsageResponse


# 일일 AI 분석 요청
class DailyAnalysisRequest(BaseModel):
    userId: str
    date: str


# 일일 AI 분석 응답
class DailyAnalysisResponse(BaseModel):
    date: str
    totalUsageSeconds: int
    mainProblem: AppCategory | None = None
    insight: str
    recommendation: str
    topApps: List[TopAppUsageResponse]
