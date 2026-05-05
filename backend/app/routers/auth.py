from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.repositories import user_repository
from app.schemas.user import GoogleLoginRequest, GoogleLoginResponse, UserResponse
from app.services.auth_service import (
    AuthConfigurationError,
    InvalidGoogleTokenError,
    create_access_token,
    verify_google_id_token,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google", response_model=GoogleLoginResponse)
def login_with_google(request: GoogleLoginRequest) -> GoogleLoginResponse:
    try:
        payload = verify_google_id_token(request.idToken)
    except AuthConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except InvalidGoogleTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google ID token.",
        ) from exc

    user = user_repository.upsert_google_user(
        provider_user_id=str(payload["sub"]),
        email=payload.get("email"),
        nickname=payload.get("name"),
    )
    try:
        access_token = create_access_token(user)
    except AuthConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    return GoogleLoginResponse(accessToken=access_token, user=user)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return current_user
