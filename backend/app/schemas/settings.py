from typing import List
from pydantic import BaseModel


class AppLimit(BaseModel):
    appName: str
    packageName: str
    category: str
    limitMinutes: int
    enabled: bool


class FocusSchedule(BaseModel):
    scheduleId: str
    title: str
    startTime: str
    endTime: str
    enabled: bool


class UserSettings(BaseModel):
    userId: str
    dailyScreenTimeGoalMinutes: int
    appLimits: List[AppLimit]
    focusSchedules: List[FocusSchedule]
    updatedAt: str


class UserSettingsUpdateRequest(BaseModel):
    dailyScreenTimeGoalMinutes: int
    appLimits: List[AppLimit]
    focusSchedules: List[FocusSchedule]


class UserSettingsResponse(BaseModel):
    success: bool = True
    settings: UserSettings


class UserSettingsUpdateResponse(BaseModel):
    success: bool = True
    message: str
    settings: UserSettings
