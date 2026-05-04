import uuid
from collections import defaultdict
from datetime import datetime

from app.schemas.analysis import DailyAnalysisResponse
from app.schemas.common import AppCategory
from app.schemas.report import (
    AICoachingReport,
    AICoachingReportCreateRequest,
    AICoachingReportCreateResponse,
    DailyTrendItem,
    RecommendedAction,
)
from app.schemas.settings import UserSettings
from app.schemas.summary import DailySummaryResponse
from app.schemas.usage_log import UsageLogResponse
from app.services.openai_analysis_service import (
    build_openai_daily_analysis,
    build_openai_weekly_analysis,
)


DISTRACTION_CATEGORIES = {
    AppCategory.ENTERTAINMENT,
    AppCategory.GAME,
    AppCategory.SNS,
}

WEEKDAY_LABELS = ["월", "화", "수", "목", "금", "토", "일"]


def build_daily_analysis(
    summary: DailySummaryResponse,
    user_settings: UserSettings | None = None,
) -> DailyAnalysisResponse:
    main_problem = _select_main_problem(summary, user_settings)
    openai_analysis = build_openai_daily_analysis(
        summary=summary,
        fallback_main_problem=main_problem,
        user_settings=user_settings,
    )
    if openai_analysis is not None:
        return openai_analysis

    return _build_local_daily_analysis(
        summary=summary,
        main_problem=main_problem,
        user_settings=user_settings,
    )


def build_weekly_analysis(
    request: AICoachingReportCreateRequest,
    logs: list[UsageLogResponse],
    user_settings: UserSettings | None = None,
) -> AICoachingReportCreateResponse:
    weekly_trend = _build_weekly_trend(logs)
    report_id = f"weekly_{uuid.uuid4().hex[:8]}"
    created_at = datetime.utcnow().isoformat()

    openai_result = build_openai_weekly_analysis(
        request=request,
        logs=logs,
        weekly_trend=weekly_trend,
        user_settings=user_settings,
    )
    if openai_result:
        report = AICoachingReport(
            reportId=report_id,
            userId=request.userId,
            startDate=request.startDate,
            endDate=request.endDate,
            summaryTitle=openai_result.get("summaryTitle", "주간 리포트"),
            summaryMessage=openai_result.get(
                "summaryMessage",
                "이번 주 스마트폰 사용 흐름을 확인해보세요.",
            ),
            focusScore=openai_result.get("focusScore", 70),
            screenTimeDeltaMinutes=openai_result.get("screenTimeDeltaMinutes", 0),
            weeklyTrend=weekly_trend,
            recommendations=[
                RecommendedAction(**rec)
                for rec in openai_result.get("recommendations", [])
            ],
            weeklyReflectionPrompt=openai_result.get(
                "weeklyReflectionPrompt",
                "다음 주에는 어떤 사용 습관을 개선하고 싶나요?",
            ),
            createdAt=created_at,
        )
    else:
        report = _build_local_weekly_report(
            request=request,
            weekly_trend=weekly_trend,
            report_id=report_id,
            created_at=created_at,
        )

    return AICoachingReportCreateResponse(
        message="weekly analysis created",
        report=report,
    )


def _build_local_daily_analysis(
    summary: DailySummaryResponse,
    main_problem: AppCategory | None,
    user_settings: UserSettings | None,
) -> DailyAnalysisResponse:
    top_app_names = ", ".join(app.appName for app in summary.topApps) or "앱 없음"
    target_usage_seconds = _calculate_target_usage_seconds(summary, user_settings)
    goal_seconds = (
        user_settings.dailyUsageGoalMinutes * 60 if user_settings is not None else None
    )

    if summary.totalUsageSeconds == 0:
        insight = "해당 날짜의 사용 로그가 아직 없습니다."
        recommendation = "일일 분석 전에 하루 사용 로그를 먼저 업로드해 주세요."
    elif goal_seconds is not None and target_usage_seconds > goal_seconds:
        over_minutes = (target_usage_seconds - goal_seconds) // 60
        insight = (
            f"목표 카테고리 사용 시간이 설정 목표보다 {over_minutes}분 많습니다. "
            f"상위 앱은 {top_app_names}입니다."
        )
        recommendation = (
            "내일은 목표 카테고리 사용을 먼저 줄이고, "
            "집중/수면 시간대 사용 여부도 함께 점검해보세요."
        )
    elif main_problem is None:
        insight = (
            "오늘 사용량은 주요 문제 카테고리에 크게 치우치지 않았습니다. "
            f"상위 앱은 {top_app_names}입니다."
        )
        recommendation = "일일 총 사용 시간을 확인하면서 설정한 목표를 유지해보세요."
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


def _build_weekly_trend(logs: list[UsageLogResponse]) -> list[DailyTrendItem]:
    daily_usage = defaultdict(int)
    for log in logs:
        daily_usage[log.date] += log.usageSeconds

    weekly_trend = []
    for date, seconds in sorted(daily_usage.items()):
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            day = WEEKDAY_LABELS[dt.weekday()]
        except ValueError:
            day = "?"
        weekly_trend.append(DailyTrendItem(day=day, date=date, minutes=seconds // 60))
    return weekly_trend


def _build_local_weekly_report(
    request: AICoachingReportCreateRequest,
    weekly_trend: list[DailyTrendItem],
    report_id: str,
    created_at: str,
) -> AICoachingReport:
    return AICoachingReport(
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
            RecommendedAction(
                title="휴식 시간 가지기",
                description="이번 주에는 스마트폰 사용을 조금 줄여보세요.",
            )
        ],
        weeklyReflectionPrompt="스마트폰 사용을 줄이기 위해 어떤 노력을 해볼 수 있을까요?",
        createdAt=created_at,
    )


def _select_main_problem(
    summary: DailySummaryResponse,
    user_settings: UserSettings | None = None,
) -> AppCategory | None:
    target_categories = (
        set(user_settings.targetCategories)
        if user_settings is not None
        else DISTRACTION_CATEGORIES
    )
    for category_summary in summary.categorySummaries:
        if category_summary.category in target_categories:
            return category_summary.category
    return summary.categorySummaries[0].category if summary.categorySummaries else None


def _calculate_target_usage_seconds(
    summary: DailySummaryResponse,
    user_settings: UserSettings | None,
) -> int:
    if user_settings is None:
        return 0
    target_categories = set(user_settings.targetCategories)
    return sum(
        item.usageSeconds
        for item in summary.categorySummaries
        if item.category in target_categories
    )
