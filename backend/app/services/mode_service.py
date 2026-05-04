from app.schemas.common import AppCategory, CoachToneType
from app.schemas.mode import DetoxModeType, ModePreset
from app.schemas.settings import AppLimit, CategoryGoal, FocusSchedule, UserSettingsUpdateRequest


def get_mode_presets() -> list[ModePreset]:
    return [
        # 1. 초급 모드: 전체 사용 시간 목표만 가볍게 설정
        ModePreset(
            mode=DetoxModeType.EASY,
            title="초급 모드 (가벼운 시작)",
            description="전체 스마트폰 사용 시간을 가볍게 의식하며 사용 습관을 관찰하는 모드입니다.",
            settingsPreset=UserSettingsUpdateRequest(
                dailyScreenTimeGoalMinutes=360,
                categoryGoals=[],
                appLimits=[],
                focusSchedules=[],
                coachTone=CoachToneType.FRIENDLY,
            ),
        ),
        # 2. 중급 모드: 주요 앱(SNS/영상)의 하루 목표 사용 시간 설정
        ModePreset(
            mode=DetoxModeType.NORMAL,
            title="중급 모드 (사용량 인지)",
            description="자주 쓰는 앱의 하루 목표 시간을 설정하여 과도한 사용을 스스로 조절하도록 유도합니다.",
            settingsPreset=UserSettingsUpdateRequest(
                dailyScreenTimeGoalMinutes=240,
                categoryGoals=[
                    CategoryGoal(
                        category=AppCategory.SNS,
                        limitMinutes=120,
                        enabled=True,
                    )
                ],
                appLimits=[
                    AppLimit(
                        appName="YouTube",
                        packageName="com.google.android.youtube",
                        category="ENTERTAINMENT",
                        limitMinutes=90,
                        enabled=True,
                    ),
                    AppLimit(
                        appName="Instagram",
                        packageName="com.instagram.android",
                        category="SNS",
                        limitMinutes=60,
                        enabled=True,
                    ),
                ],
                focusSchedules=[
                    FocusSchedule(
                        scheduleId="sleep_normal",
                        title="수면 시간",
                        startTime="23:30",
                        endTime="07:00",
                        enabled=True,
                    )
                ],
                coachTone=CoachToneType.INNOCENT,
            ),
        ),
        # 3. 고급 모드: 강도 높은 목표 설정으로 확실한 사용 시간 단축
        ModePreset(
            mode=DetoxModeType.HARD,
            title="고급 모드 (확실한 단축)",
            description="앱 사용 목표 시간을 타이트하게 설정하여 스마트폰 밖의 일상에 온전히 집중하도록 돕습니다.",
            settingsPreset=UserSettingsUpdateRequest(
                dailyScreenTimeGoalMinutes=120,
                categoryGoals=[
                    CategoryGoal(
                        category=AppCategory.ENTERTAINMENT,
                        limitMinutes=60,
                        enabled=True,
                    )
                ],
                appLimits=[
                    AppLimit(
                        appName="YouTube",
                        packageName="com.google.android.youtube",
                        category="ENTERTAINMENT",
                        limitMinutes=45,
                        enabled=True,
                    ),
                    AppLimit(
                        appName="Instagram",
                        packageName="com.instagram.android",
                        category="SNS",
                        limitMinutes=30,
                        enabled=True,
                    ),
                ],
                focusSchedules=[
                    FocusSchedule(
                        scheduleId="sleep_hard",
                        title="수면 시간",
                        startTime="22:30",
                        endTime="07:00",
                        enabled=True,
                    ),
                    FocusSchedule(
                        scheduleId="focus_work",
                        title="집중 시간",
                        startTime="09:00",
                        endTime="18:00",
                        enabled=True,
                    ),
                ],
                coachTone=CoachToneType.STRICT,
            ),
        ),
    ]
