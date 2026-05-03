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
    load_dotenv(PROJECT_DIR / ".env")
    load_dotenv(BACKEND_DIR / ".env", override=True)


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


settings = Settings()
