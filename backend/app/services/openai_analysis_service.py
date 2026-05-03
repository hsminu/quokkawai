import json

from app.config import settings
from app.schemas.analysis import DailyAnalysisResponse
from app.schemas.common import AppCategory
from app.schemas.summary import DailySummaryResponse


def build_openai_daily_analysis(
    summary: DailySummaryResponse,
    fallback_main_problem: AppCategory | None,
) -> DailyAnalysisResponse | None:
    if not settings.openai_api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=settings.openai_api_key)
    summary_json = json.dumps(summary.model_dump(mode="json"), ensure_ascii=False)

    try:
        response = client.responses.create(
            model=settings.openai_model,
            instructions=(
                "You are Quokkawai's daily smartphone usage coach. "
                "Return only JSON. Write insight and recommendation in Korean. "
                "Be concise, practical, and non-judgmental."
            ),
            input=(
                "Analyze this daily smartphone usage summary and return JSON with "
                "exactly these keys: mainProblem, insight, recommendation. "
                "mainProblem must be one of STUDY, PRODUCTIVITY, COMMUNICATION, "
                "ENTERTAINMENT, GAME, SNS, SYSTEM, ETC, or null.\n\n"
                f"Summary:\n{summary_json}"
            ),
            max_output_tokens=500,
        )
    except Exception:
        return None

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


def _parse_category(value: object) -> AppCategory | None:
    if value is None:
        return None
    try:
        return AppCategory(str(value))
    except ValueError:
        return None


def _strip_json_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```json"):
        return stripped.removeprefix("```json").removesuffix("```").strip()
    if stripped.startswith("```"):
        return stripped.removeprefix("```").removesuffix("```").strip()
    return stripped
