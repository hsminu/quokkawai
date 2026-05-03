from app.schemas.app_category import AppCategoryResponse
from app.schemas.common import AppCategory


# AI 분류 전에 먼저 확인하는 기본 앱 카테고리 목록
DEFAULT_APP_CATEGORIES = [
    AppCategoryResponse(
        packageName="com.google.android.youtube",
        appName="YouTube",
        category=AppCategory.ENTERTAINMENT,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.instagram.android",
        appName="Instagram",
        category=AppCategory.SNS,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.nhn.android.webtoon",
        appName="Naver Webtoon",
        category=AppCategory.ENTERTAINMENT,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.kakao.talk",
        appName="KakaoTalk",
        category=AppCategory.COMMUNICATION,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.google.android.gm",
        appName="Gmail",
        category=AppCategory.COMMUNICATION,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.google.android.calendar",
        appName="Google Calendar",
        category=AppCategory.PRODUCTIVITY,
        isUserDefined=False,
    ),
    AppCategoryResponse(
        packageName="com.android.settings",
        appName="Settings",
        category=AppCategory.SYSTEM,
        isUserDefined=False,
    ),
]


# 이 prefix로 시작하면 시스템 앱으로 분류한다.
SYSTEM_PACKAGE_PREFIXES = (
    "com.android.",
    "com.google.android.gms",
    "com.google.android.inputmethod",
    "com.samsung.android.app.launcher",
)


def build_usage_log_id(user_id: str, date: str, package_name: str) -> str:
    # 같은 사용자/날짜/앱은 같은 문서 ID를 사용한다.
    return f"{user_id}_{date}_{package_name}"
