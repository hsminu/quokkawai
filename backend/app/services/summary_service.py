from collections import defaultdict

from app.schemas.summary import (
    CategoryUsageResponse,
    DailySummaryResponse,
    ScheduleUsageResponse,
    TopAppUsageResponse,
)
from app.schemas.usage_log import UsageLogResponse


def build_daily_summary(date: str, logs: list[UsageLogResponse]) -> DailySummaryResponse:
    # 하루 전체 사용 시간
    total_usage_seconds = sum(log.usageSeconds for log in logs)

    # 많이 사용한 앱 상위 3개
    top_apps = [
        TopAppUsageResponse(
            packageName=log.packageName,
            appName=log.appName,
            category=log.category,
            usageSeconds=log.usageSeconds,
        )
        for log in sorted(logs, key=lambda item: item.usageSeconds, reverse=True)[:3]
    ]

    # 카테고리별 사용 시간 합계
    category_seconds = defaultdict(int)
    for log in logs:
        category_seconds[log.category] += log.usageSeconds

    # 많이 사용한 카테고리 순서로 정렬
    category_summaries = [
        CategoryUsageResponse(category=category, usageSeconds=usage_seconds)
        for category, usage_seconds in sorted(
            category_seconds.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    ]

    # 집중/수면 스케줄 시간대별 사용량 합계
    schedule_seconds = defaultdict(int)
    for log in logs:
        if log.scheduleId:
            schedule_seconds[log.scheduleId] += log.usageSeconds

    schedule_summaries = [
        ScheduleUsageResponse(scheduleId=sid, usageSeconds=secs)
        for sid, secs in schedule_seconds.items()
    ]

    return DailySummaryResponse(
        date=date,
        totalUsageSeconds=total_usage_seconds,
        topApps=top_apps,
        categorySummaries=category_summaries,
        scheduleSummaries=schedule_summaries,
    )
