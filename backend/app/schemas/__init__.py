from app.schemas.analysis import DailyAnalysisRequest, DailyAnalysisResponse
from app.schemas.app_category import (
    AppCategoryListResponse,
    AppCategoryResponse,
    AppCategoryUpdateRequest,
    AppCategoryUpdateResponse,
)
from app.schemas.common import (
    AppCategory,
    CoachToneType,
    ErrorDetail,
    ErrorResponse,
    ListResponse,
    SuccessMessageResponse,
)
from app.schemas.mode import DetoxModeType, ModeListResponse, ModePreset
from app.schemas.report import (
    AICoachingReport,
    AICoachingReportCreateRequest,
    AICoachingReportCreateResponse,
    AppUsageSummary,
    DailyReport,
    DailyTrendItem,
    HomeReportResponse,
    HomeUserSummary,
    RecommendedAction,
    WeeklyReport,
    WeeklyReportResponse,
)
from app.schemas.settings import (
    AppLimit,
    CategoryGoal,
    FocusSchedule,
    UserSettings,
    UserSettingsResponse,
    UserSettingsUpdateRequest,
    UserSettingsUpdateResponse,
)
from app.schemas.summary import (
    CategoryUsageResponse,
    DailySummaryResponse,
    ScheduleUsageResponse,
    TopAppUsageResponse,
)
from app.schemas.usage_log import (
    UsageLogBulkCreateRequest,
    UsageLogBulkCreateResponse,
    UsageLogCreateItem,
    UsageLogCreateRequest,
    UsageLogCreateResponse,
    UsageLogListResponse,
    UsageLogResponse,
)
from app.schemas.user import GoogleLoginRequest, GoogleLoginResponse, UserResponse

__all__ = [
    "AppCategory",
    "AppCategoryListResponse",
    "AppCategoryResponse",
    "AppCategoryUpdateRequest",
    "AppCategoryUpdateResponse",
    "CategoryUsageResponse",
    "DailyAnalysisRequest",
    "DailyAnalysisResponse",
    "DailySummaryResponse",
    "ErrorResponse",
    # user
    "GoogleLoginRequest",
    "GoogleLoginResponse",
    "TopAppUsageResponse",
    "UsageLogBulkCreateRequest",
    "UsageLogBulkCreateResponse",
    "UsageLogCreateItem",
    "UsageLogCreateRequest",
    "UsageLogCreateResponse",
    "UsageLogListResponse",
    "UsageLogResponse",
    "UserResponse",
]
