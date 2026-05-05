import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from typing import Any

from app.config import settings
from app.schemas.user import UserResponse


class AuthConfigurationError(RuntimeError):
    pass


class InvalidGoogleTokenError(RuntimeError):
    pass


class InvalidAccessTokenError(RuntimeError):
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


def create_access_token(user: UserResponse) -> str:
    if not settings.jwt_secret_key:
        raise AuthConfigurationError("JWT_SECRET_KEY is not configured.")

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {
        "sub": user.userId,
        "provider": user.provider,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    return _encode_jwt(payload, settings.jwt_secret_key)


def verify_access_token(token: str) -> dict[str, Any]:
    if not settings.jwt_secret_key:
        raise AuthConfigurationError("JWT_SECRET_KEY is not configured.")

    parts = token.split(".")
    if len(parts) != 3:
        raise InvalidAccessTokenError("Invalid access token.")

    signing_input = f"{parts[0]}.{parts[1]}".encode("ascii")
    expected_signature = _sign(signing_input, settings.jwt_secret_key)
    try:
        actual_signature = _base64url_decode(parts[2])
    except ValueError as exc:
        raise InvalidAccessTokenError("Invalid access token.") from exc

    if not hmac.compare_digest(actual_signature, expected_signature):
        raise InvalidAccessTokenError("Invalid access token.")

    try:
        payload = json.loads(_base64url_decode(parts[1]))
    except (ValueError, json.JSONDecodeError) as exc:
        raise InvalidAccessTokenError("Invalid access token.") from exc

    expires_at = payload.get("exp")
    if not isinstance(expires_at, int):
        raise InvalidAccessTokenError("Invalid access token.")
    if expires_at < int(datetime.now(timezone.utc).timestamp()):
        raise InvalidAccessTokenError("Access token expired.")
    if not payload.get("sub"):
        raise InvalidAccessTokenError("Invalid access token.")
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


def _encode_jwt(payload: dict[str, Any], secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = _base64url_encode(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = _base64url_encode(
        json.dumps(payload, separators=(",", ":")).encode()
    )
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = _base64url_encode(_sign(signing_input, secret))
    return f"{encoded_header}.{encoded_payload}.{signature}"


def _sign(signing_input: bytes, secret: str) -> bytes:
    return hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()


def _base64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)
