from app.schemas.analysis import DailyAnalysisResponse
from app.schemas.common import AppCategory
from app.schemas.summary import DailySummaryResponse


# MVP에서 문제 카테고리로 볼 항목
DISTRACTION_CATEGORIES = {
    AppCategory.ENTERTAINMENT,
    AppCategory.GAME,
    AppCategory.SNS,
}


def build_daily_analysis(summary: DailySummaryResponse) -> DailyAnalysisResponse:
    # 지금은 OpenAI 연결 전이라 요약 데이터로 간단한 문장만 생성
    main_problem = _select_main_problem(summary)
    top_app_names = ", ".join(app.appName for app in summary.topApps) or "no apps"

    if summary.totalUsageSeconds == 0:
        insight = "No usage logs were found for this date."
        recommendation = "Upload daily usage logs before requesting an analysis."
    elif main_problem is None:
        insight = (
            f"Your largest usage today was balanced outside the main distraction "
            f"categories. Top apps: {top_app_names}."
        )
        recommendation = "Keep reviewing daily totals and protect your focused blocks."
    else:
        insight = (
            f"{main_problem.value} took the largest share of today's usage. "
            f"Top apps: {top_app_names}."
        )
        recommendation = (
            f"Try reducing {main_problem.value} usage by 30 minutes tomorrow and "
            "move one session to a planned break."
        )

    return DailyAnalysisResponse(
        date=summary.date,
        totalUsageSeconds=summary.totalUsageSeconds,
        mainProblem=main_problem,
        insight=insight,
        recommendation=recommendation,
        topApps=summary.topApps,
    )


def _select_main_problem(summary: DailySummaryResponse) -> AppCategory | None:
    # 산만함 카테고리가 있으면 그중 가장 많이 쓴 카테고리를 선택
    for category_summary in summary.categorySummaries:
        if category_summary.category in DISTRACTION_CATEGORIES:
            return category_summary.category
    # 없으면 가장 많이 쓴 카테고리를 대표값으로 사용
    return summary.categorySummaries[0].category if summary.categorySummaries else None
