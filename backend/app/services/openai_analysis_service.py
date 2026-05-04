import json

from app.config import settings
from app.schemas.analysis import DailyAnalysisResponse
from app.schemas.common import AppCategory, CoachToneType
from app.schemas.report import AICoachingReportCreateRequest, DailyTrendItem
from app.schemas.summary import DailySummaryResponse
from app.schemas.usage_log import UsageLogResponse


def build_openai_daily_analysis(
    summary: DailySummaryResponse,
    fallback_main_problem: AppCategory | None,
    coach_tone: CoachToneType,
) -> DailyAnalysisResponse | None:
    # OpenAI 키가 없으면 로컬 대체 분석을 쓰게 한다.
    if not settings.openai_api_key:
        return None

    tone_instruction = {
        CoachToneType.FRIENDLY: "친한 친구처럼 편안하고 다정한 반말로 작성하세요.",
        CoachToneType.STRICT: "엄격하고 단호한 아버지처럼 무게감 있고 따끔하게 충고하는 말투로 작성하세요.",
        CoachToneType.INNOCENT: "순진하고 엉뚱한 요정이나 아이처럼 귀엽고 순수한 말투로 작성하세요.",
    }.get(coach_tone, "간결하고 실용적이며 비난하지 않는 톤을 유지하세요.")

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=settings.openai_api_key)
    summary_json = json.dumps(summary.model_dump(mode="json"), ensure_ascii=False)

    try:
        # 요약 데이터만 보내고, 결과는 JSON으로 받는다.
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"당신은 Quokkawai의 일일 스마트폰 사용 코치입니다.\n"
                        f"말투 지시사항: {tone_instruction}\n"
                        "JSON만 반환하세요. insight와 recommendation은 지정된 말투로 작성하세요."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "다음 일일 스마트폰 사용 요약을 분석하고, "
                        "mainProblem, insight, recommendation 키만 가진 JSON을 반환하세요. "
                        "mainProblem은 STUDY, PRODUCTIVITY, COMMUNICATION, ENTERTAINMENT, "
                        "GAME, SNS, SYSTEM, ETC 중 하나이거나 null이어야 합니다. "
                        "특히 요약 데이터에 수면 시간이나 집중 시간(scheduleSummaries)의 사용량이 존재한다면, 그 시간대의 스마트폰 사용에 대해 반드시 코멘트해주세요.\n\n"
                        f"요약:\n{summary_json}"
                    ),
                },
            ],
            max_tokens=500,
        )
    except Exception:
        return None

    # 모델 응답을 DailyAnalysisResponse로 변환한다.
    content = _strip_json_fence(response.choices[0].message.content)
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
) -> dict | None:
    if not settings.openai_api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=settings.openai_api_key)

    tone_instruction = {
        CoachToneType.FRIENDLY: "친한 친구처럼 편안하고 다정한 반말로 작성하세요.",
        CoachToneType.STRICT: "엄격하고 단호한 아버지처럼 무게감 있고 따끔하게 충고하는 말투로 작성하세요.",
        CoachToneType.INNOCENT: "순진하고 엉뚱한 요정이나 아이처럼 귀엽고 순수한 말투로 작성하세요.",
    }.get(request.coachTone, "간결하고 실용적이며 비난하지 않는 톤을 유지하세요.")

    trend_data = [{"date": t.date, "minutes": t.minutes} for t in weekly_trend]
    trend_json = json.dumps(trend_data, ensure_ascii=False)

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"당신은 Quokkawai의 주간 스마트폰 사용 코치입니다.\n"
                        f"말투 지시사항: {tone_instruction}\n"
                        "JSON만 반환하세요. 피드백 텍스트는 지정된 말투(한국어)로 작성하세요."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "다음은 주간 스마트폰 사용 요약입니다. "
                        "summaryTitle, summaryMessage, focusScore (0-100), screenTimeDeltaMinutes (지난주 대비 변화량 추정), "
                        "recommendations (title과 description을 포함한 객체 리스트), weeklyReflectionPrompt 키를 가진 JSON을 반환하세요.\n\n"
                        f"기간: {request.startDate} ~ {request.endDate}\n"
                        f"일별 사용량(분):\n{trend_json}"
                    ),
                },
            ],
            max_tokens=800,
        )
    except Exception:
        return None

    content = _strip_json_fence(response.choices[0].message.content)
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


def _strip_json_fence(text: str) -> str:
    # 혹시 ```json 코드블록으로 오면 JSON 본문만 남긴다.
    stripped = text.strip()
    if stripped.startswith("```json"):
        return stripped.removeprefix("```json").removesuffix("```").strip()
    if stripped.startswith("```"):
        return stripped.removeprefix("```").removesuffix("```").strip()
    return stripped
