from datetime import datetime
from fastapi import APIRouter, Query

from app.repositories import user_settings_repository
from app.schemas.common import CoachToneType
from app.schemas.settings import (
    UserSettings,
    UserSettingsResponse,
    UserSettingsUpdateRequest,
    UserSettingsUpdateResponse,
)

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=UserSettingsResponse)
def get_user_settings(userId: str = Query(...)) -> UserSettingsResponse:
    settings = user_settings_repository.get_settings(user_id=userId)
    
    # 사용자가 저장한 설정이 없다면 기본값을 만들어 내려줍니다.
    if not settings:
        settings = UserSettings(
            userId=userId,
            dailyScreenTimeGoalMinutes=360,
            categoryGoals=[],
            appLimits=[],
            focusSchedules=[],
            coachTone=CoachToneType.FRIENDLY,
            updatedAt=datetime.utcnow().isoformat(),
        )
    return UserSettingsResponse(success=True, settings=settings)


@router.put("", response_model=UserSettingsUpdateResponse)
def update_user_settings(
    request: UserSettingsUpdateRequest,
    userId: str = Query(...),
) -> UserSettingsUpdateResponse:
    settings = user_settings_repository.update_settings(user_id=userId, request=request)
    return UserSettingsUpdateResponse(
        success=True,
        message="user settings updated",
        settings=settings,
    )