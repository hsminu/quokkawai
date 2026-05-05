from typing import List

from pydantic import BaseModel

from app.schemas.common import AppCategory
from app.schemas.summary import TopAppUsageResponse


class DailyAnalysisRequest(BaseModel):
    userId: str
    date: str


class DailyAnalysisMeRequest(BaseModel):
    date: str


class DailyAnalysisResponse(BaseModel):
    date: str
    totalUsageSeconds: int
    mainProblem: AppCategory | None = None
    insight: str
    recommendation: str
    topApps: List[TopAppUsageResponse]
