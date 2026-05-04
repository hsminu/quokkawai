from typing import List
from pydantic import BaseModel

from app.schemas.common import CoachToneType

###########################################
# 홈 리포트, 7일 리포트, AI 코칭 리포트 타입
###########################################


# 홈 화면이나 AI 리포트에서 보여줄 추천 행동 카드
class RecommendedAction(BaseModel):
    title: str
    description: str


# 앱 사용량 요약 정보
# 주간 리포트의 많이 사용한 앱 목록 등에 사용.
class AppUsageSummary(BaseModel):
    appName: str
    packageName: str | None = None
    category: str
    usageSeconds: int


# 하루 단위 리포트
# 홈 화면에서 사용하는 핵심 데이터
class DailyReport(BaseModel):
    reportId: str
    userId: str
    date: str
    streakDays: int

    # 목표 대비 사용률, 75: 목표의 75% 사용을 의미
    goalAchievementRate: int

    statusTitle: str
    statusMessage: str
    focusTimeMinutes: int
    remainingGoals: int

    # 휴대폰 잠금 해제 횟수, Optional 처리
    unlockCount: int | None = None

    screenTimeMinutes: int
    coachMessage: str
    recommendedActions: List[RecommendedAction]
    createdAt: str

# 홈 화면에 함께 내려줄 사용자 요약 정보
class HomeUserSummary(BaseModel):
    userId: str
    name: str | None = None
    profileImageUrl: str | None = None


# 홈 화면 리포트 API 응답
class HomeReportResponse(BaseModel):
    success: bool = True
    user: HomeUserSummary
    report: DailyReport


# 주간 그래프에 사용할 하루 단위 데이터
class DailyTrendItem(BaseModel):
    day: str
    date: str
    minutes: int


# 7일 분석 화면에서 사용하는 주간 리포트
class WeeklyReport(BaseModel):
    reportId: str
    userId: str
    startDate: str
    endDate: str
    coachTone: CoachToneType = CoachToneType.FRIENDLY
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


# 주간 리포트 API 응답
class WeeklyReportResponse(BaseModel):
    success: bool = True
    report: WeeklyReport

# AI 코칭 리포트
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


# AI 코칭 리포트 생성 요청
class AICoachingReportCreateRequest(BaseModel):
    userId: str
    startDate: str
    endDate: str


# AI 코칭 리포트 조회 응답
class AICoachingReportResponse(BaseModel):
    success: bool = True
    report: AICoachingReport


# AI 코칭 리포트 생성 응답
class AICoachingReportCreateResponse(BaseModel):
    success: bool = True
    message: str
    report: AICoachingReport
