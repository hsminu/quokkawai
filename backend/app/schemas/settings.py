from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from app.schemas.common import AppCategory


class AnalysisMode(str, Enum):
    FOCUS = "FOCUS"
    SLEEP = "SLEEP"


class AnalysisTone(str, Enum):
    SOFT = "SOFT"
    FRIENDLY = "FRIENDLY"
    DIRECT = "DIRECT"


class AnalysisSchedule(BaseModel):
    scheduleId: str
    mode: AnalysisMode
    title: str
    startTime: str
    endTime: str
    enabled: bool = True


def default_target_categories() -> List[AppCategory]:
    return [
        AppCategory.SNS,
        AppCategory.GAME,
        AppCategory.ENTERTAINMENT,
    ]


class UserSettings(BaseModel):
    userId: str
    dailyUsageGoalMinutes: int = Field(..., gt=0)
    targetCategories: List[AppCategory] = Field(default_factory=default_target_categories)
    analysisSchedules: List[AnalysisSchedule] = Field(default_factory=list)
    analysisTone: AnalysisTone = AnalysisTone.SOFT
    updatedAt: str


class UserSettingsUpdateRequest(BaseModel):
    dailyUsageGoalMinutes: int = Field(..., gt=0)
    targetCategories: List[AppCategory] = Field(default_factory=default_target_categories)
    analysisSchedules: List[AnalysisSchedule] = Field(default_factory=list)
    analysisTone: AnalysisTone = AnalysisTone.SOFT


class UserSettingsResponse(BaseModel):
    success: bool = True
    settings: UserSettings


class UserSettingsUpdateResponse(BaseModel):
    success: bool = True
    message: str
    settings: UserSettings
