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
                "Android 앱을 정확히 하나의 카테고리로 분류하세요. "
                "설명 없이 enum 값만 반환하세요."
            ),
            input=(
                "다음 enum 중 하나를 고르세요: "
                "STUDY, PRODUCTIVITY, COMMUNICATION, ENTERTAINMENT, GAME, SNS, "
                "SYSTEM, ETC.\n\n"
                f"앱 이름: {app_name}\n"
                f"패키지명: {package_name}"
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
