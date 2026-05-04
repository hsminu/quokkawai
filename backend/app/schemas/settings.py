from typing import List
from pydantic import BaseModel

from app.schemas.common import AppCategory, CoachToneType


#############################
# 목표 설정 화면 데이터 타입
##############################

# 문제 카테고리(SNS, GAME 등) 전체 사용 목표
class CategoryGoal(BaseModel):
    category: AppCategory
    limitMinutes: int
    enabled: bool


# 앱별 사용 제한 설정
class AppLimit(BaseModel):
    appName: str
    packageName: str
    category: str
    limitMinutes: int
    enabled: bool


# 집중모드/수면모드 같은 시간대 설정
class FocusSchedule(BaseModel):
    scheduleId: str
    title: str
    startTime: str
    endTime: str
    enabled: bool


# 사용자 설정 전체 데이터
class UserSettings(BaseModel):
    userId: str

    # 하루 전체 화면 사용 목표, 시간 / 단위:분
    dailyScreenTimeGoalMinutes: int

    # 카테고리별 목표 목록
    categoryGoals: List[CategoryGoal]

    # 앱별 제한 목록
    appLimits: List[AppLimit]

    # 집중모드/수면모드 일정 목록
    focusSchedules: List[FocusSchedule]

    # AI 코치 말투
    coachTone: CoachToneType

    # 설정 마지막 수정 시각
    updatedAt: str



# 사용자 설정 수정 요청
class UserSettingsUpdateRequest(BaseModel):
    dailyScreenTimeGoalMinutes: int
    categoryGoals: List[CategoryGoal]
    appLimits: List[AppLimit]
    focusSchedules: List[FocusSchedule]
    coachTone: CoachToneType


# 사용자 설정 조회 응답
class UserSettingsResponse(BaseModel):
    success: bool = True
    settings: UserSettings


# 사용자 설정 저장/수정 응답
class UserSettingsUpdateResponse(BaseModel):
    success: bool = True
    message: str
    settings: UserSettings
