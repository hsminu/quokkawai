from typing import List

from pydantic import BaseModel

from app.schemas.common import AppCategory


# 많이 사용한 앱 한 개의 요약
class TopAppUsageResponse(BaseModel):
    packageName: str
    appName: str
    category: AppCategory
    usageSeconds: int


# 카테고리별 사용 시간 요약
class CategoryUsageResponse(BaseModel):
    category: AppCategory
    usageSeconds: int


# 하루 사용량 요약 응답
class DailySummaryResponse(BaseModel):
    date: str
    totalUsageSeconds: int
    topApps: List[TopAppUsageResponse]
    categorySummaries: List[CategoryUsageResponse]
