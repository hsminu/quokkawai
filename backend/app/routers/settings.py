from fastapi import APIRouter, Query

from app.repositories import settings_repository
from app.schemas.settings import (
    UserSettingsResponse,
    UserSettingsUpdateRequest,
    UserSettingsUpdateResponse,
)


router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=UserSettingsResponse)
def get_user_settings(userId: str = Query(...)) -> UserSettingsResponse:
    settings = settings_repository.get_by_user_id(userId)
    return UserSettingsResponse(settings=settings)


@router.put("", response_model=UserSettingsUpdateResponse)
def update_user_settings(
    request: UserSettingsUpdateRequest,
    userId: str = Query(...),
) -> UserSettingsUpdateResponse:
    settings = settings_repository.save(user_id=userId, request=request)
    return UserSettingsUpdateResponse(
        message="user settings saved",
        settings=settings,
    )
