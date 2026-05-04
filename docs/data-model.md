# Data Model

## 1. 목적

이 문서는 Quokkawai 서비스에서 사용하는 주요 데이터 개념을 정의한다.

이 문서는 Firestore의 실제 컬렉션 구조를 설명하는 문서가 아니라, 서비스에서 다루는 핵심 데이터 모델의 의미와 관계를 설명하는 문서이다.

Firestore의 실제 저장 구조는 `db-schema.md`에서 정의한다.

---

## 2. 모델 목록

Quokkawai MVP에서 사용하는 주요 데이터 모델은 다음과 같다.

```text
User
UsageLog
UserSettings
ModePreset
AppCategory
DailySummary
DailyAnalysis
```

---

## 3. User

### 3.1 설명

User는 Quokkawai 서비스를 사용하는 사용자를 의미한다.

최종 구현에서는 Google OAuth 로그인 정보를 기반으로 생성된다.

---

### 3.2 주요 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| userId | string | 서버 내부 사용자 ID |
| provider | string | 로그인 제공자. MVP에서는 google |
| providerUserId | string | Google 계정 고유 ID |
| email | string/null | 사용자 이메일 |
| nickname | string/null | 사용자 표시 이름 |
| createdAt | datetime | 생성 시간 |
| updatedAt | datetime | 수정 시간 |

---

### 3.3 비고

초기 개발 단계에서는 더미 userId를 사용할 수 있다.

예시:

```text
test_user_001
```

Google 로그인 연동 이후에는 클라이언트가 userId를 직접 보내지 않고, 서버가 인증 토큰에서 userId를 추출한다.

---

## 4. UsageLog

### 4.1 설명

UsageLog는 사용자의 특정 날짜 앱별 사용량 요약 데이터이다.

MVP에서는 세션 단위 로그를 저장하지 않는다. 즉, 앱을 몇 시부터 몇 시까지 사용했는지를 저장하지 않고, 하루 동안 특정 앱을 총 몇 초 사용했는지를 저장한다.

---

### 4.2 예시

```json
{
  "userId": "test_user_001",
  "date": "2026-05-01",
  "packageName": "com.google.android.youtube",
  "appName": "YouTube",
  "category": "ENTERTAINMENT",
  "usageSeconds": 5400,
  "openCount": 12
}
```

---

### 4.3 주요 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| usageLogId | string | 사용 로그 ID |
| userId | string | 사용자 ID |
| date | string | 사용 날짜. YYYY-MM-DD |
| packageName | string | Android 앱 패키지명 |
| appName | string | 앱 표시 이름 |
| category | string | 앱 카테고리 |
| usageSeconds | int | 앱 사용 시간. 초 단위 |
| openCount | int | 앱 실행 횟수 |
| scheduleId | string/null | 수면/집중 모드 등 활성화된 스케줄 ID |
| createdAt | datetime | 생성 시간 |
| updatedAt | datetime | 수정 시간 |

---

### 4.4 설계 결정

```text
UsageLog는 세션 로그가 아니라 하루 앱별 요약 로그이다.
minutesUsed는 사용하지 않는다.
usageSeconds를 표준 시간 단위로 사용한다.
category는 클라이언트가 결정하지 않고 서버가 packageName 기준으로 결정한다.
```

---

## 5. UserSettings & ModePreset

### 5.1 설명

`UserSettings`는 사용자가 선택한 디톡스 목표(시간, 앱, 카테고리), 집중 스케줄, 그리고 AI 코치의 말투 페르소나 정보를 담는다.
`ModePreset`은 사용자가 쉽게 목표를 시작할 수 있도록 시스템이 제공하는 초급/중급/고급 단위의 프리셋 모델이다.

---

### 5.2 UserSettings 주요 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| userId | string | 사용자 ID |
| dailyScreenTimeGoalMinutes | int | 하루 스마트폰 전체 사용 목표 시간(분) |
| categoryGoals | array | `CategoryGoal` (카테고리별 목표) 목록 |
| appLimits | array | `AppLimit` (특정 앱 제한) 목록 |
| focusSchedules | array | `FocusSchedule` (수면/집중 시간대) 목록 |
| coachTone | string | AI 코치 말투 (`FRIENDLY`, `STRICT`, `INNOCENT`) |
| updatedAt | datetime | 설정 마지막 업데이트 시간 |

---

### 5.3 AI 페르소나(CoachToneType)

| 값 | 의미 |
|---|---|
| FRIENDLY | 친한 친구처럼 편안하고 다정한 반말 |
| STRICT | 엄격하고 단호한 아버지처럼 충고하는 말투 |
| INNOCENT | 순진하고 엉뚱한 요정처럼 귀여운 말투 |

---

## 6. AppCategory

### 6.1 설명

AppCategory는 앱 패키지명과 카테고리의 매핑 정보이다.

서버는 packageName을 기준으로 앱의 카테고리를 결정한다.

---

### 6.2 카테고리 목록

MVP에서 사용하는 카테고리는 다음 8개이다.

```text
STUDY
PRODUCTIVITY
COMMUNICATION
ENTERTAINMENT
GAME
SNS
SYSTEM
ETC
```

---

### 6.3 카테고리 설명

| 값 | 의미 | 예시 |
|---|---|---|
| STUDY | 공부 | 강의 앱, Anki, 클래스룸 |
| PRODUCTIVITY | 생산성 | 캘린더, 노션, 메모, 문서 앱 |
| COMMUNICATION | 커뮤니케이션 | 카카오톡, 메시지, Gmail, Slack |
| ENTERTAINMENT | 엔터테인먼트 | YouTube, Netflix, Webtoon, 음악 앱 |
| GAME | 게임 | 모바일 게임 |
| SNS | SNS | Instagram, X, TikTok, Facebook |
| SYSTEM | 시스템 | 설정, 런처, 키보드 |
| ETC | 기타 | 분류 불가 앱 |

---

### 6.4 주요 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| packageName | string | Android 앱 패키지명 |
| appName | string | 앱 표시 이름 |
| category | string | 앱 카테고리 enum |
| isUserDefined | boolean | 사용자가 직접 수정했는지 여부 |
| createdAt | datetime | 생성 시간 |
| updatedAt | datetime | 수정 시간 |

---

### 6.5 비고

서버에는 영어 enum 값을 저장한다.

Flutter 앱에서는 enum 값을 한국어 라벨로 변환하여 표시한다.

예시:

```text
ENTERTAINMENT -> 엔터테인먼트
PRODUCTIVITY -> 생산성
```

---

## 7. DailySummary

### 7.1 설명

DailySummary는 특정 사용자의 특정 날짜 사용량 요약 데이터이다.

DailySummary는 UsageLog를 기반으로 계산된다.

---

### 7.2 예시

```json
{
  "userId": "test_user_001",
  "date": "2026-05-01",
  "totalUsageSeconds": 14400,
  "topApps": [
    {
      "packageName": "com.google.android.youtube",
      "appName": "YouTube",
      "category": "ENTERTAINMENT",
      "usageSeconds": 5400
    }
  ],
  "categorySummaries": [
    {
      "category": "ENTERTAINMENT",
      "usageSeconds": 7800
    }
  ],
  "scheduleSummaries": [
    {
      "scheduleId": "sleep_normal",
      "usageSeconds": 1800
    }
  ]
}
```

---

### 7.3 주요 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| userId | string | 사용자 ID |
| date | string | 요약 날짜 |
| totalUsageSeconds | int | 하루 총 사용 시간 |
| topApps | array | 사용량 상위 앱 목록 |
| categorySummaries | array | 카테고리별 사용량 요약 |
| scheduleSummaries | array | 수면/집중 스케줄 시간대별 사용량 요약 |
| createdAt | datetime | 생성 시간 |
| updatedAt | datetime | 수정 시간 |

---

### 7.4 비고

MVP에서는 DailySummary를 별도 컬렉션에 반드시 저장하지 않아도 된다.

초기 구현에서는 요청 시 UsageLog를 조회하여 즉시 계산해도 된다. 다만 응답 속도와 재사용을 위해 추후 daily_summaries 컬렉션에 저장할 수 있다.

---

## 8. DailyAnalysis & AICoachingReport

### 8.1 설명

`DailyAnalysis`는 특정 날짜의 사용 요약을 바탕으로 AI가 생성한 피드백이다.
`AICoachingReport`는 시작일과 종료일(보통 7일) 기간의 트렌드를 요약하여 생성된 주간 AI 피드백이다.

---

### 8.2 예시

```json
{
  "userId": "test_user_001",
  "date": "2026-05-01",
  "coachTone": "STRICT",
  "mainProblem": "ENTERTAINMENT",
  "insight": "오늘은 YouTube와 Webtoon 사용 시간이 길어 엔터테인먼트 앱 사용 비중이 높았습니다.",
  "recommendation": "내일은 엔터테인먼트 앱 사용 시간을 1시간 줄이는 것을 목표로 해보는 것이 좋습니다."
}
```

---

### 8.3 주요 필드

| 필드 | 타입 | 설명 |
|---|---|---|
| userId | string | 사용자 ID |
| date | string | 분석 날짜 |
| coachTone | string | 분석 생성 시 적용된 AI 페르소나 |
| mainProblem | string/null | 가장 사용 비중이 높은 카테고리 또는 문제 카테고리 |
| insight | string | AI 분석 문장 |
| recommendation | string | 행동 추천 문장 |
| createdAt | datetime | 생성 시간 |
| updatedAt | datetime | 수정 시간 |

---

### 8.4 비고

AI는 원본 사용 로그를 직접 분석하지 않는다.

서버가 먼저 DailySummary 형태로 데이터를 요약한 뒤, 요약 데이터만 AI에 전달한다.

---

## 현재 구현 메모

### AppCategory 분류 흐름

`AppCategory`는 Flutter 클라이언트가 아니라 백엔드가 결정한다.

현재 MVP는 다음 분류 흐름을 사용한다.

```text
기존 packageName 매핑
-> SYSTEM package prefix 규칙
-> 모르는 일반 앱에 대한 OpenAI 분류
-> ETC 대체 분류
```

OpenAI가 모르는 앱을 분류하면 해당 카테고리를 앱 카테고리 저장소에 저장하고 이후 재사용한다.

### DailyAnalysis 생성

`DailyAnalysis`는 `DailySummary`를 기반으로 생성한다.

OpenAI에는 요약된 사용 데이터만 전달한다.

```text
date
totalUsageSeconds
topApps
categorySummaries
```

MVP에서는 백엔드가 원본 세션 단위 로그를 OpenAI에 보내지 않는다.
