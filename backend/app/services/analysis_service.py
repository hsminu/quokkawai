from app.schemas.analysis import DailyAnalysisResponse
from app.schemas.common import AppCategory
from app.schemas.summary import DailySummaryResponse
from app.services.openai_analysis_service import build_openai_daily_analysis


# Categories treated as the main distraction candidates.
DISTRACTION_CATEGORIES = {
    AppCategory.ENTERTAINMENT,
    AppCategory.GAME,
    AppCategory.SNS,
}


def build_daily_analysis(summary: DailySummaryResponse) -> DailyAnalysisResponse:
    main_problem = _select_main_problem(summary)
    openai_analysis = build_openai_daily_analysis(
        summary=summary,
        fallback_main_problem=main_problem,
    )
    if openai_analysis is not None:
        return openai_analysis

    # Fallback used when OpenAI is not configured or the API call fails.
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
    # Pick the highest-usage distraction category first.
    for category_summary in summary.categorySummaries:
        if category_summary.category in DISTRACTION_CATEGORIES:
            return category_summary.category
    # If there is no distraction category, use the top category as a representative.
    return summary.categorySummaries[0].category if summary.categorySummaries else None
