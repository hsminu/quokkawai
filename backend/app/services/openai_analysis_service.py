import json

from app.config import settings
from app.schemas.analysis import DailyAnalysisResponse
from app.schemas.common import AppCategory
from app.schemas.report import AICoachingReportCreateRequest, DailyTrendItem
from app.schemas.settings import UserSettings
from app.schemas.summary import DailySummaryResponse
from app.schemas.usage_log import UsageLogResponse


def build_openai_daily_analysis(
    summary: DailySummaryResponse,
    fallback_main_problem: AppCategory | None,
    user_settings: UserSettings | None = None,
) -> DailyAnalysisResponse | None:
    # OpenAI 키가 없으면 로컬 대체 분석을 쓰게 한다.
    if not settings.openai_api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=settings.openai_api_key)
    summary_json = json.dumps(summary.model_dump(mode="json"), ensure_ascii=False)
    settings_json = (
        json.dumps(user_settings.model_dump(mode="json"), ensure_ascii=False)
        if user_settings is not None
        else "null"
    )
    tone_instruction = _build_tone_instruction(user_settings)

    try:
        # 요약 데이터만 보내고, 결과는 JSON으로 받는다.
        response = client.responses.create(
            model=settings.openai_model,
            instructions=(
                "당신은 Quokkawai의 일일 스마트폰 사용 코치입니다. "
                "JSON만 반환하세요. insight와 recommendation은 한국어로 작성하세요. "
                f"{tone_instruction}"
            ),
            input=(
                "다음 일일 스마트폰 사용 요약을 분석하고, "
                "mainProblem, insight, recommendation 키만 가진 JSON을 반환하세요. "
                "mainProblem은 STUDY, PRODUCTIVITY, COMMUNICATION, ENTERTAINMENT, "
                "GAME, SNS, SYSTEM, ETC 중 하나이거나 null이어야 합니다.\n\n"
                "사용자 설정은 dailyUsageGoalMinutes, targetCategories, analysisSchedules, analysisTone을 포함합니다. "
                "targetCategories의 총 사용 시간이 dailyUsageGoalMinutes를 넘었는지 우선 확인하세요. "
                "analysisSchedules의 FOCUS/SLEEP 시간대는 앱 차단 규칙이 아니라 분석 참고 맥락으로만 쓰세요.\n\n"
                f"요약:\n{summary_json}\n\n"
                f"사용자 설정:\n{settings_json}"
            ),
            max_output_tokens=500,
        )
    except Exception:
        return None

    # 모델 응답을 DailyAnalysisResponse로 변환한다.
    content = _strip_json_fence(response.output_text)
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return None

    main_problem = _parse_category(data.get("mainProblem")) or fallback_main_problem
    insight = data.get("insight")
    recommendation = data.get("recommendation")
    if not isinstance(insight, str) or not isinstance(recommendation, str):
        return None

    return DailyAnalysisResponse(
        date=summary.date,
        totalUsageSeconds=summary.totalUsageSeconds,
        mainProblem=main_problem,
        insight=insight,
        recommendation=recommendation,
        topApps=summary.topApps,
    )


def build_openai_weekly_analysis(
    request: AICoachingReportCreateRequest,
    logs: list[UsageLogResponse],
    weekly_trend: list[DailyTrendItem],
    user_settings: UserSettings | None = None,
) -> dict | None:
    if not settings.openai_api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=settings.openai_api_key)

    trend_data = [{"date": t.date, "minutes": t.minutes} for t in weekly_trend]
    trend_json = json.dumps(trend_data, ensure_ascii=False)
    settings_json = (
        json.dumps(user_settings.model_dump(mode="json"), ensure_ascii=False)
        if user_settings is not None
        else "null"
    )
    tone_instruction = _build_tone_instruction(user_settings)

    try:
        response = client.responses.create(
            model=settings.openai_model,
            instructions=(
                "당신은 Quokkawai의 주간 스마트폰 사용 코치입니다. "
                "JSON만 반환하세요. 내용은 한국어로 작성하세요. "
                f"{tone_instruction}"
            ),
            input=(
                "다음은 주간 스마트폰 사용 요약입니다. "
                "summaryTitle, summaryMessage, focusScore (0-100), screenTimeDeltaMinutes (지난주 대비 변화량 추정), "
                "recommendations (title과 description을 포함한 객체 리스트), weeklyReflectionPrompt 키를 가진 JSON을 반환하세요.\n\n"
                f"기간: {request.startDate} ~ {request.endDate}\n"
                f"일별 사용량(분):\n{trend_json}\n\n"
                f"사용자 설정:\n{settings_json}"
            ),
            max_output_tokens=800,
        )
    except Exception:
        return None

    content = _strip_json_fence(response.output_text)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


def _parse_category(value: object) -> AppCategory | None:
    # 모델이 준 문자열을 서버 enum으로 변환한다.
    if value is None:
        return None
    try:
        return AppCategory(str(value))
    except ValueError:
        return None


def _build_tone_instruction(user_settings: UserSettings | None) -> str:
    if user_settings is None:
        tone = "SOFT"
    else:
        tone = user_settings.analysisTone.value

    if tone == "FRIENDLY":
        return (
            "친한 친구처럼 편하고 다정하게 말하세요. "
            "반말에 가까운 자연스러운 한국어를 쓰되, 사용자를 놀리거나 과하게 가볍게 대하지 마세요."
        )
    if tone == "DIRECT":
        return (
            "직설적이고 명확하게 말하세요. "
            "문제와 다음 행동을 바로 짚되, 모욕적이거나 비난하는 표현은 쓰지 마세요."
        )
    return (
        "부드럽고 차분한 말투로 말하세요. "
        "간결하고 실용적이며 비난하지 않는 톤을 유지하세요."
    )


def _strip_json_fence(text: str) -> str:
    # 혹시 ```json 코드블록으로 오면 JSON 본문만 남긴다.
    stripped = text.strip()
    if stripped.startswith("```json"):
        return stripped.removeprefix("```json").removesuffix("```").strip()
    if stripped.startswith("```"):
        return stripped.removeprefix("```").removesuffix("```").strip()
    return stripped
