from fastapi import Header, HTTPException, status

from app.repositories import user_repository
from app.schemas.user import UserResponse
from app.services.auth_service import (
    AuthConfigurationError,
    InvalidAccessTokenError,
    verify_access_token,
)


def get_current_user(authorization: str = Header(...)) -> UserResponse:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
        )

    try:
        payload = verify_access_token(token)
    except AuthConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except InvalidAccessTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    user = user_repository.get_by_user_id(str(payload["sub"]))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )
    return user
