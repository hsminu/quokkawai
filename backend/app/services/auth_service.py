from typing import Any

from app.config import settings
from app.schemas.user import UserResponse


class AuthConfigurationError(RuntimeError):
    pass


class InvalidGoogleTokenError(RuntimeError):
    pass


def verify_google_id_token(id_token: str) -> dict[str, Any]:
    if not settings.google_client_id:
        raise AuthConfigurationError("GOOGLE_CLIENT_ID is not configured.")

    try:
        from google.auth.transport import requests
        from google.oauth2 import id_token as google_id_token
    except ImportError as exc:
        raise AuthConfigurationError("google-auth package is not installed.") from exc

    try:
        payload = google_id_token.verify_oauth2_token(
            id_token,
            requests.Request(),
            settings.google_client_id,
        )
    except ValueError as exc:
        raise InvalidGoogleTokenError("Invalid Google ID token.") from exc

    if not payload.get("sub"):
        raise InvalidGoogleTokenError("Google ID token does not contain sub.")
    return payload


def build_google_user_from_payload(payload: dict[str, Any]) -> UserResponse:
    provider_user_id = str(payload["sub"])
    return UserResponse(
        userId=f"google_{provider_user_id}",
        provider="google",
        providerUserId=provider_user_id,
        email=payload.get("email"),
        nickname=payload.get("name"),
    )
