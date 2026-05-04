from app.config import settings
from app.schemas.common import AppCategory


def classify_app_category(package_name: str, app_name: str) -> AppCategory | None:
    # OpenAI 키가 없으면 호출하지 않고 None을 반환한다.
    if not settings.openai_api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=settings.openai_api_key)

    try:
        # 앱 이름과 패키지명만 보내서 enum 하나만 받는다.
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Android 앱을 정확히 하나의 카테고리로 분류하세요. "
                        "설명 없이 enum 값만 반환하세요."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "다음 enum 중 하나를 고르세요: "
                        "STUDY, PRODUCTIVITY, COMMUNICATION, ENTERTAINMENT, GAME, SNS, "
                        "SYSTEM, ETC.\n\n"
                        f"앱 이름: {app_name}\n"
                        f"패키지명: {package_name}"
                    ),
                },
            ],
            max_tokens=20,
        )
    except Exception:
        return None

    return _parse_category(response.choices[0].message.content)


def _parse_category(value: str | None) -> AppCategory | None:
    # 모델이 설명을 붙이지 않았다는 가정하에 enum 값만 정리한다.
    if not value:
        return None
    cleaned = value.strip().strip('"').strip("'").upper()
    try:
        return AppCategory(cleaned)
    except ValueError:
        return None
