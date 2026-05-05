from fastapi import APIRouter, HTTPException, status

from app.repositories import user_repository
from app.schemas.user import GoogleLoginRequest, GoogleLoginResponse
from app.services.auth_service import (
    AuthConfigurationError,
    InvalidGoogleTokenError,
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
    return GoogleLoginResponse(user=user)
