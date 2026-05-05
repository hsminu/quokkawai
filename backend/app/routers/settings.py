from fastapi import APIRouter, Depends, Query

from app.dependencies import get_current_user
from app.repositories import settings_repository
from app.schemas.settings import (
    UserSettingsResponse,
    UserSettingsUpdateRequest,
    UserSettingsUpdateResponse,
)
from app.schemas.user import UserResponse


router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/me", response_model=UserSettingsResponse)
def get_my_settings(
    current_user: UserResponse = Depends(get_current_user),
) -> UserSettingsResponse:
    settings = settings_repository.get_by_user_id(current_user.userId)
    return UserSettingsResponse(settings=settings)


@router.put("/me", response_model=UserSettingsUpdateResponse)
def update_my_settings(
    request: UserSettingsUpdateRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> UserSettingsUpdateResponse:
    settings = settings_repository.save(user_id=current_user.userId, request=request)
    return UserSettingsUpdateResponse(
        message="user settings saved",
        settings=settings,
    )


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
