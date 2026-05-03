import json

from app.config import settings
from app.schemas.analysis import DailyAnalysisResponse
from app.schemas.common import AppCategory
from app.schemas.summary import DailySummaryResponse


def build_openai_daily_analysis(
    summary: DailySummaryResponse,
    fallback_main_problem: AppCategory | None,
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

    try:
        # 요약 데이터만 보내고, 결과는 JSON으로 받는다.
        response = client.responses.create(
            model=settings.openai_model,
            instructions=(
                "당신은 Quokkawai의 일일 스마트폰 사용 코치입니다. "
                "JSON만 반환하세요. insight와 recommendation은 한국어로 작성하세요. "
                "간결하고 실용적이며 비난하지 않는 톤을 유지하세요."
            ),
            input=(
                "다음 일일 스마트폰 사용 요약을 분석하고, "
                "mainProblem, insight, recommendation 키만 가진 JSON을 반환하세요. "
                "mainProblem은 STUDY, PRODUCTIVITY, COMMUNICATION, ENTERTAINMENT, "
                "GAME, SNS, SYSTEM, ETC 중 하나이거나 null이어야 합니다.\n\n"
                f"요약:\n{summary_json}"
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
