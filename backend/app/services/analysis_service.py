import uuid
from collections import defaultdict
from datetime import datetime

from app.schemas.analysis import DailyAnalysisResponse
from app.schemas.common import AppCategory, CoachToneType
from app.schemas.report import (
    AICoachingReport,
    AICoachingReportCreateRequest,
    AICoachingReportCreateResponse,
    DailyTrendItem,
    RecommendedAction,
)
from app.schemas.summary import DailySummaryResponse
from app.schemas.usage_log import UsageLogResponse
from app.services.openai_analysis_service import (
    build_openai_daily_analysis,
    build_openai_weekly_analysis,
)


# 문제 카테고리 후보로 볼 항목
DISTRACTION_CATEGORIES = {
    AppCategory.ENTERTAINMENT,
    AppCategory.GAME,
    AppCategory.SNS,
}


def build_daily_analysis(summary: DailySummaryResponse, coach_tone: CoachToneType) -> DailyAnalysisResponse:
    main_problem = _select_main_problem(summary)
    openai_analysis = build_openai_daily_analysis(
        summary=summary,
        fallback_main_problem=main_problem,
        coach_tone=coach_tone,
    )
    if openai_analysis is not None:
        return openai_analysis

    # OpenAI 실패 시 간단한 로컬 분석을 반환한다.
    top_app_names = ", ".join(app.appName for app in summary.topApps) or "앱 없음"

    if summary.totalUsageSeconds == 0:
        insight = "해당 날짜의 사용 로그가 아직 없습니다."
        recommendation = "일일 분석을 요청하기 전에 하루 사용 로그를 먼저 업로드해 주세요."
    elif main_problem is None:
        insight = (
            f"오늘 사용량은 주요 산만함 카테고리에 크게 치우치지 않았습니다. "
            f"상위 앱은 {top_app_names}입니다."
        )
        recommendation = "일일 총 사용 시간을 계속 확인하면서 집중 시간대를 지켜보세요."
    else:
        insight = (
            f"오늘은 {main_problem.value} 카테고리의 사용 비중이 가장 컸습니다. "
            f"상위 앱은 {top_app_names}입니다."
        )
        recommendation = (
            f"내일은 {main_problem.value} 사용 시간을 30분 줄이고, "
            "한 번의 사용 세션을 미리 정한 휴식 시간으로 옮겨보세요."
        )

    return DailyAnalysisResponse(
        date=summary.date,
        totalUsageSeconds=summary.totalUsageSeconds,
        mainProblem=main_problem,
        insight=insight,
        recommendation=recommendation,
        topApps=summary.topApps,
    )


def build_weekly_analysis(
    request: AICoachingReportCreateRequest,
    logs: list[UsageLogResponse],
) -> AICoachingReportCreateResponse:
    daily_usage = defaultdict(int)
    for log in logs:
        daily_usage[log.date] += log.usageSeconds

    weekly_trend = []
    for date, seconds in sorted(daily_usage.items()):
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            day_str = ["월", "화", "수", "목", "금", "토", "일"][dt.weekday()]
        except ValueError:
            day_str = "?"
        weekly_trend.append(DailyTrendItem(day=day_str, date=date, minutes=seconds // 60))

    report_id = f"weekly_{uuid.uuid4().hex[:8]}"
    created_at = datetime.utcnow().isoformat()

    openai_result = build_openai_weekly_analysis(request, logs, weekly_trend)

    if openai_result:
        report = AICoachingReport(
            reportId=report_id,
            userId=request.userId,
            startDate=request.startDate,
            endDate=request.endDate,
            summaryTitle=openai_result.get("summaryTitle", "주간 리포트"),
            summaryMessage=openai_result.get("summaryMessage", "이번 주 앱 사용량을 확인해보세요."),
            focusScore=openai_result.get("focusScore", 70),
            screenTimeDeltaMinutes=openai_result.get("screenTimeDeltaMinutes", 0),
            weeklyTrend=weekly_trend,
            recommendations=[
                RecommendedAction(**rec) for rec in openai_result.get("recommendations", [])
            ],
            weeklyReflectionPrompt=openai_result.get("weeklyReflectionPrompt", "다음 주에는 어떤 습관을 개선하고 싶나요?"),
            createdAt=created_at,
        )
    else:
        report = AICoachingReport(
            reportId=report_id,
            userId=request.userId,
            startDate=request.startDate,
            endDate=request.endDate,
            summaryTitle="주간 사용량 분석",
            summaryMessage="주간 사용량이 집계되었습니다. 스마트폰 사용 시간을 확인해보세요.",
            focusScore=50,
            screenTimeDeltaMinutes=0,
            weeklyTrend=weekly_trend,
            recommendations=[
                RecommendedAction(title="휴식 시간 가지기", description="주말에는 스마트폰 사용을 줄여보세요.")
            ],
            weeklyReflectionPrompt="스마트폰 사용을 줄이기 위해 어떤 노력을 할 수 있을까요?",
            createdAt=created_at,
        )

    return AICoachingReportCreateResponse(
        message="weekly analysis created",
        report=report,
    )


def _select_main_problem(summary: DailySummaryResponse) -> AppCategory | None:
    # 산만함 카테고리가 있으면 사용량이 가장 큰 항목을 선택한다.
    for category_summary in summary.categorySummaries:
        if category_summary.category in DISTRACTION_CATEGORIES:
            return category_summary.category
    # 없으면 가장 많이 사용한 카테고리를 대표값으로 사용한다.
    return summary.categorySummaries[0].category if summary.categorySummaries else None
