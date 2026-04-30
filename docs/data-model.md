# 데이터 모델 명세서

## 1. MVP 데이터 모델 최종안

Quokkawai MVP에서 사용하는 핵심 데이터 모델은 다음 6개로 확정한다.

```text
users
user_settings
usage_logs
daily_reports
weekly_reports
ai_coaching_reports
```

MVP에서는 구글 로그인만 지원한다.  
비밀번호 기반 회원가입, 이메일 로그인, 카카오 로그인, 애플 로그인은 구현하지 않는다.

친구, 구독, 고객센터, 푸시 알림은 MVP 범위에서 제외한다.  
프론트 화면에 존재하더라도 초기 백엔드에서는 더미 데이터로 처리한다.

---

## 2. users

사용자 기본 정보를 저장한다.  
Quokkawai는 MVP에서 구글 로그인만 지원하므로 비밀번호는 저장하지 않는다.

### 예시

```json
{
  "userId": "user_001",
  "googleUserId": "109238471928374",
  "email": "quokka@gmail.com",
  "name": "강현욱",
  "profileImageUrl": "https://example.com/profile.png",
  "createdAt": "2026-04-29T12:00:00",
  "updatedAt": "2026-04-29T12:00:00",
  "lastLoginAt": "2026-04-30T09:00:00"
}
```

### 필드 설명

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| userId | string | O | 앱 내부 사용자 고유 ID |
| googleUserId | string | O | 구글 계정 고유 ID |
| email | string | X | 구글 계정 이메일 |
| name | string | X | 구글 계정 표시 이름 |
| profileImageUrl | string | X | 구글 프로필 이미지 URL |
| createdAt | datetime | O | 생성 시각 |
| updatedAt | datetime | O | 수정 시각 |
| lastLoginAt | datetime | O | 마지막 로그인 시각 |

### 주의사항

비밀번호 원문과 `passwordHash`는 저장하지 않는다.  
사용자 식별은 `googleUserId`를 기준으로 처리한다.  
DB에서는 `googleUserId`에 unique 제약을 둔다.

---

## 3. user_settings

사용자의 목표 설정 정보를 저장한다.  
목표 설정 화면의 일일 화면 사용 목표, 앱별 사용 제한, 집중모드 일정, 수면 모드 예약에 사용된다.

### 예시

```json
{
  "userId": "user_001",
  "dailyScreenTimeGoalMinutes": 210,
  "appLimits": [
    {
      "appName": "Instagram",
      "packageName": "com.instagram.android",
      "category": "소셜 미디어",
      "limitMinutes": 45,
      "enabled": true
    },
    {
      "appName": "YouTube",
      "packageName": "com.google.android.youtube",
      "category": "엔터테인먼트",
      "limitMinutes": 60,
      "enabled": true
    }
  ],
  "focusSchedules": [
    {
      "scheduleId": "focus_001",
      "title": "오전 집중 업무",
      "startTime": "09:00",
      "endTime": "11:00",
      "enabled": true
    },
    {
      "scheduleId": "sleep_001",
      "title": "수면 준비 시간",
      "startTime": "22:00",
      "endTime": "07:00",
      "enabled": false
    }
  ],
  "updatedAt": "2026-04-29T12:00:00"
}
```

### 필드 설명

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| userId | string | O | 사용자 ID |
| dailyScreenTimeGoalMinutes | number | O | 하루 전체 화면 사용 목표 시간 |
| appLimits | array | O | 앱별 제한 목록 |
| focusSchedules | array | O | 집중모드 및 수면모드 일정 목록 |
| updatedAt | datetime | O | 수정 시각 |

### appLimits 내부 구조

```json
{
  "appName": "Instagram",
  "packageName": "com.instagram.android",
  "category": "소셜 미디어",
  "limitMinutes": 45,
  "enabled": true
}
```

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| appName | string | O | 앱 이름 |
| packageName | string | O | 앱 패키지명 |
| category | string | O | 앱 카테고리 |
| limitMinutes | number | O | 제한 시간 |
| enabled | boolean | O | 제한 활성화 여부 |

### focusSchedules 내부 구조

```json
{
  "scheduleId": "focus_001",
  "title": "오전 집중 업무",
  "startTime": "09:00",
  "endTime": "11:00",
  "enabled": true
}
```

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| scheduleId | string | O | 일정 ID |
| title | string | O | 일정 이름 |
| startTime | string | O | 시작 시간 |
| endTime | string | O | 종료 시간 |
| enabled | boolean | O | 활성화 여부 |

---

## 4. usage_logs

Android에서 수집한 실제 앱 사용 로그를 저장한다.  
앱별 사용 시간, 실행 횟수, 알림 수 등의 원천 데이터 역할을 한다.

### 예시

```json
{
  "logId": "log_001",
  "userId": "user_001",
  "date": "2026-04-29",
  "appName": "YouTube",
  "packageName": "com.google.android.youtube",
  "category": "엔터테인먼트",
  "minutesUsed": 92,
  "openCount": 12,
  "notificationCount": 30,
  "timeOfDay": "night",
  "createdAt": "2026-04-29T23:59:00"
}
```

### 필드 설명

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| logId | string | O | 로그 ID |
| userId | string | O | 사용자 ID |
| date | string | O | 날짜 |
| appName | string | O | 앱 이름 |
| packageName | string | O | 앱 패키지명 |
| category | string | X | 앱 카테고리 |
| minutesUsed | number | O | 사용 시간 |
| openCount | number | X | 앱 실행 횟수 |
| notificationCount | number | X | 알림 수 |
| timeOfDay | string | X | 사용 시간대 |
| createdAt | datetime | O | 생성 시각 |

### 주의사항

`minutesUsed`는 필수다.  
`openCount`, `notificationCount`는 Android에서 수집이 어려울 수 있으므로 선택값으로 둔다.

---

## 5. daily_reports

홈 화면을 위한 하루 요약 데이터를 저장한다.  
오늘의 현황, 목표 달성률, 코치 메시지, 추천 활동 등에 사용된다.

### 예시

```json
{
  "reportId": "daily_20260429_user001",
  "userId": "user_001",
  "date": "2026-04-29",
  "streakDays": 5,
  "goalAchievementRate": 75,
  "statusTitle": "슬슬 조절하셔야합니다?",
  "statusMessage": "오늘 제한의 75%를 완료했습니다",
  "focusTimeMinutes": 252,
  "remainingGoals": 2,
  "unlockCount": 42,
  "screenTimeMinutes": 330,
  "coachMessage": "어제보다 스마트폰 사용 시간이 15분 줄어들었습니다.",
  "recommendedActions": [
    {
      "title": "딥 워크 모드",
      "description": "모든 알림을 45분간 차단합니다"
    },
    {
      "title": "마음 챙김 명상",
      "description": "눈의 피로를 풀고 5분간 휴식"
    }
  ],
  "createdAt": "2026-04-29T23:59:00"
}
```

### 필드 설명

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| reportId | string | O | 리포트 ID |
| userId | string | O | 사용자 ID |
| date | string | O | 날짜 |
| streakDays | number | O | 연속 목표 달성 일수 |
| goalAchievementRate | number | O | 목표 사용량 대비 진행률 |
| statusTitle | string | O | 홈 카드 제목 |
| statusMessage | string | O | 홈 카드 설명 |
| focusTimeMinutes | number | O | 집중 시간 |
| remainingGoals | number | O | 남은 목표 수 |
| unlockCount | number | X | 휴대폰 확인 횟수 |
| screenTimeMinutes | number | O | 총 스크린 타임 |
| coachMessage | string | O | 퀴카코치 메시지 |
| recommendedActions | array | O | 추천 활동 |
| createdAt | datetime | O | 생성 시각 |

---

## 6. weekly_reports

7일 분석 화면을 위한 주간 요약 데이터를 저장한다.  
사용 트렌드, 평균 사용 시간, 밸런스 점수, 많이 사용한 앱 목록 등에 사용된다.

### 예시

```json
{
  "reportId": "weekly_20260423_20260429_user001",
  "userId": "user_001",
  "startDate": "2026-04-23",
  "endDate": "2026-04-29",
  "averageScreenTimeMinutes": 342,
  "changeRateFromLastWeek": 12,
  "unlockCount": 142,
  "notificationCount": 840,
  "balanceScore": 72,
  "balanceComment": "디지털 밸런스가 좋아지고 있어요. 자기 전 소셜 미디어 사용을 줄여보세요.",
  "dailyTrend": [
    {
      "day": "월",
      "date": "2026-04-23",
      "minutes": 250
    },
    {
      "day": "화",
      "date": "2026-04-24",
      "minutes": 310
    }
  ],
  "topApps": [
    {
      "appName": "YouTube",
      "packageName": "com.google.android.youtube",
      "category": "엔터테인먼트",
      "minutesUsed": 760
    },
    {
      "appName": "Instagram",
      "packageName": "com.instagram.android",
      "category": "소셜 미디어",
      "minutesUsed": 495
    }
  ],
  "coachAdvice": "이번 목요일에 평소보다 유튜브를 45% 더 많이 사용하셨습니다.",
  "createdAt": "2026-04-29T23:59:00"
}
```

### 필드 설명

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| reportId | string | O | 주간 리포트 ID |
| userId | string | O | 사용자 ID |
| startDate | string | O | 시작 날짜 |
| endDate | string | O | 종료 날짜 |
| averageScreenTimeMinutes | number | O | 일평균 사용시간 |
| changeRateFromLastWeek | number | X | 지난주 대비 변화율 |
| unlockCount | number | X | 잠금 해제 횟수 |
| notificationCount | number | X | 알림 수 |
| balanceScore | number | O | 디지털 밸런스 점수 |
| balanceComment | string | O | 밸런스 코멘트 |
| dailyTrend | array | O | 요일별 사용량 |
| topApps | array | O | 가장 많이 사용한 앱 |
| coachAdvice | string | O | 코치 조언 |
| createdAt | datetime | O | 생성 시각 |

---

## 7. ai_coaching_reports

AI 코칭 리포트 화면을 위한 분석 결과를 저장한다.  
AI 요약 메시지, 집중 점수, 추천 활동, 주간 회고 문구 등에 사용된다.

### 예시

```json
{
  "reportId": "ai_20260423_20260429_user001",
  "userId": "user_001",
  "startDate": "2026-04-23",
  "endDate": "2026-04-29",
  "summaryTitle": "잘하고 있어요!",
  "summaryMessage": "이번 주에 심야 스크롤 시간을 15% 줄이셨네요. 숙면에 큰 도움이 될 거예요!",
  "focusScore": 82,
  "screenTimeDeltaMinutes": -80,
  "weeklyTrend": [
    {
      "day": "월",
      "date": "2026-04-23",
      "minutes": 310
    },
    {
      "day": "화",
      "date": "2026-04-24",
      "minutes": 280
    }
  ],
  "recommendations": [
    {
      "title": "수면 경계 설정",
      "description": "오후 10시 이후 소셜 미디어 제한"
    },
    {
      "title": "앱 시간 제한",
      "description": "인스타그램 30분 제한 추가"
    },
    {
      "title": "마음 챙김 휴식",
      "description": "5분 호흡 운동 해보기"
    }
  ],
  "weeklyReflectionPrompt": "이번 주 디지털 밸런스는 어땠나요? 잠시 되돌아보는 시간은 더 좋은 습관을 만드는 데 도움이 됩니다.",
  "createdAt": "2026-04-29T23:59:00"
}
```

### 필드 설명

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| reportId | string | O | AI 리포트 ID |
| userId | string | O | 사용자 ID |
| startDate | string | O | 시작 날짜 |
| endDate | string | O | 종료 날짜 |
| summaryTitle | string | O | AI 요약 제목 |
| summaryMessage | string | O | AI 요약 메시지 |
| focusScore | number | O | 집중 점수 |
| screenTimeDeltaMinutes | number | O | 스크린 타임 변화량 |
| weeklyTrend | array | O | 주간 사용 트렌드 |
| recommendations | array | O | 추천 활동 |
| weeklyReflectionPrompt | string | O | 주간 회고 문구 |
| createdAt | datetime | O | 생성 시각 |

---

## 8. 공통 타입 규칙

### 날짜

```text
YYYY-MM-DD
```

예시:

```text
2026-04-29
```

### 시간

```text
HH:mm
```

예시:

```text
09:00
```

### datetime

```text
ISO 8601
```

예시:

```text
2026-04-29T23:59:00
```

---

## 9. 카테고리 목록

초기 카테고리는 아래 목록으로 고정한다.

```text
공부
생산성
커뮤니케이션
정보검색
소셜 미디어
엔터테인먼트
쇼츠/도파민
게임
기타
```

프론트, 백엔드, AI는 반드시 이 카테고리 목록만 사용한다.  
`SNS`, `소셜`, `소셜 미디어`처럼 표현이 섞이면 데이터가 불안정해지므로 하나로 통일한다.

---

## 10. MVP 모델 요약

| 모델 | 역할 |
|---|---|
| users | 구글 로그인 사용자 정보 |
| user_settings | 목표 시간, 앱별 제한, 집중모드 일정 |
| usage_logs | Android에서 올라오는 원천 사용 기록 |
| daily_reports | 홈 화면용 하루 요약 |
| weekly_reports | 7일 분석 화면용 요약 |
| ai_coaching_reports | AI 코칭 리포트 화면용 요약 |

---

## 11. MVP에서 제외하는 모델

아래 모델은 MVP에서 제외한다.

```text
friends
rankings
subscriptions
notifications
customer_support
privacy_settings
app_versions
password_auth
email_auth
kakao_auth
apple_auth
```

프론트 화면에 표시할 수는 있지만, 초기 백엔드에서는 더미 데이터로 처리한다.

---

## 12. 최종 확정

Quokkawai MVP 데이터 모델은 다음 6개로 확정한다.

```text
1. users
2. user_settings
3. usage_logs
4. daily_reports
5. weekly_reports
6. ai_coaching_reports
```

인증 방식은 구글 로그인만 사용한다.

```text
구글 로그인 성공
→ googleUserId 확인
→ users에서 googleUserId 조회
→ 기존 사용자가 있으면 로그인 처리
→ 없으면 신규 users 문서 생성
```

다음 단계는 이 데이터 모델을 기준으로 API 명세서를 확장 작성하는 것이다.

```text
docs/api-spec.md
```
