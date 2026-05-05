import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - only happens before dependencies install
    load_dotenv = None


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent

if load_dotenv is not None:
    # 루트 .env보다 backend/.env 값을 우선한다.
    load_dotenv(PROJECT_DIR / ".env")
    load_dotenv(BACKEND_DIR / ".env", override=True)


@dataclass(frozen=True)
class Settings:
    # memory 또는 firestore
    database_backend: str = os.getenv("DATABASE_BACKEND", "memory")
    # Firebase 서비스 계정 JSON 경로
    firebase_credentials_path: str | None = (
        os.getenv("FIREBASE_CREDENTIALS_PATH")
        or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    # Firebase 프로젝트 ID
    firebase_project_id: str | None = (
        os.getenv("FIREBASE_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    # OpenAI API 설정
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
    # Google OAuth ID Token 검증에 사용할 client id
    google_client_id: str | None = os.getenv("GOOGLE_CLIENT_ID")
    # 서버가 발급하는 access token 서명 설정
    jwt_secret_key: str | None = os.getenv("JWT_SECRET_KEY")
    jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "10080"))


settings = Settings()
