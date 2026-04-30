from typing import List
from pydantic import BaseModel


class RecommendedAction(BaseModel):
    title: str
    description: str


class AppUsageSummary(BaseModel):
    appName: str
    packageName: str | None = None
    category: str
    minutesUsed: int


class DailyReport(BaseModel):
    reportId: str
    userId: str
    date: str
    streakDays: int
    goalAchievementRate: int
    statusTitle: str
    statusMessage: str
    focusTimeMinutes: int
    remainingGoals: int
    unlockCount: int | None = None
    screenTimeMinutes: int
    coachMessage: str
    recommendedActions: List[RecommendedAction]
    createdAt: str


class HomeUserSummary(BaseModel):
    userId: str
    name: str | None = None
    profileImageUrl: str | None = None


class HomeReportResponse(BaseModel):
    success: bool = True
    user: HomeUserSummary
    report: DailyReport


class DailyTrendItem(BaseModel):
    day: str
    date: str
    minutes: int


class WeeklyReport(BaseModel):
    reportId: str
    userId: str
    startDate: str
    endDate: str
    averageScreenTimeMinutes: int
    changeRateFromLastWeek: int | None = None
    unlockCount: int | None = None
    notificationCount: int | None = None
    balanceScore: int
    balanceComment: str
    dailyTrend: List[DailyTrendItem]
    topApps: List[AppUsageSummary]
    coachAdvice: str
    createdAt: str


class WeeklyReportResponse(BaseModel):
    success: bool = True
    report: WeeklyReport


class AICoachingReport(BaseModel):
    reportId: str
    userId: str
    startDate: str
    endDate: str
    summaryTitle: str
    summaryMessage: str
    focusScore: int
    screenTimeDeltaMinutes: int
    weeklyTrend: List[DailyTrendItem]
    recommendations: List[RecommendedAction]
    weeklyReflectionPrompt: str
    createdAt: str


class AICoachingReportCreateRequest(BaseModel):
    userId: str
    startDate: str
    endDate: str


class AICoachingReportResponse(BaseModel):
    success: bool = True
    report: AICoachingReport


class AICoachingReportCreateResponse(BaseModel):
    success: bool = True
    message: str
    report: AICoachingReport
