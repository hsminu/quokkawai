from app.config import settings
from app.schemas.common import AppCategory


def classify_app_category(package_name: str, app_name: str) -> AppCategory | None:
    if not settings.openai_api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=settings.openai_api_key)

    try:
        response = client.responses.create(
            model=settings.openai_model,
            instructions=(
                "Classify an Android app into exactly one category. "
                "Return only the enum value, no explanation."
            ),
            input=(
                "Choose one category from this enum: "
                "STUDY, PRODUCTIVITY, COMMUNICATION, ENTERTAINMENT, GAME, SNS, "
                "SYSTEM, ETC.\n\n"
                f"App name: {app_name}\n"
                f"Package name: {package_name}"
            ),
            max_output_tokens=20,
        )
    except Exception:
        return None

    return _parse_category(response.output_text)


def _parse_category(value: str) -> AppCategory | None:
    cleaned = value.strip().strip('"').strip("'").upper()
    try:
        return AppCategory(cleaned)
    except ValueError:
        return None
