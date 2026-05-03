# DTO / Schema Specification

## 1. 목적

이 문서는 Quokkawai 백엔드와 Flutter 앱이 주고받는 요청/응답 데이터 형식을 정의한다.

API 경로와 전체 흐름은 `api-spec.md`를 기준으로 한다.

---

## 2. 공통 규칙

### 2.1 필드 네이밍

API 요청/응답에서는 camelCase를 사용한다.

예시:

```json
{
  "packageName": "com.google.android.youtube",
  "usageSeconds": 5400
}
```

Python 내부에서는 snake_case를 사용할 수 있다.

예시:

```python
package_name: str
usage_seconds: int
```

---

### 2.2 날짜 형식

날짜는 `YYYY-MM-DD` 문자열을 사용한다.

```json
{
  "date": "2026-05-01"
}
```

---

### 2.3 시간 단위

사용 시간은 초 단위로 표현한다.

```json
{
  "usageSeconds": 5400
}
```

`minutesUsed`는 사용하지 않는다.

---

### 2.4 카테고리 enum

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

## 3. Common Schema

### 3.1 ErrorResponse

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid request body",
    "detail": "usageSeconds must be greater than 0"
  }
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| error | object | O | 에러 객체 |

---

### 3.2 ErrorDetail

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| code | string | O | 에러 코드 |
| message | string | O | 에러 요약 메시지 |
| detail | string/null | X | 상세 설명 |

---

## 4. User Schema

### 4.1 UserResponse

```json
{
  "userId": "user_001",
  "provider": "google",
  "providerUserId": "google-sub-value",
  "email": "user@example.com",
  "nickname": "user nickname"
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| userId | string | O | 서버 내부 사용자 ID |
| provider | string | O | 로그인 제공자 |
| providerUserId | string | O | Google 계정 고유 ID |
| email | string/null | X | 이메일 |
| nickname | string/null | X | 표시 이름 |

---

## 5. Auth Schema

### 5.1 GoogleLoginRequest

```json
{
  "idToken": "google-id-token-value"
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| idToken | string | O | Google ID Token |

---

### 5.2 GoogleLoginResponse

```json
{
  "accessToken": "server-access-token",
  "tokenType": "bearer",
  "user": {
    "userId": "user_001",
    "provider": "google",
    "providerUserId": "google-sub-value",
    "email": "user@example.com",
    "nickname": "user nickname"
  }
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| accessToken | string | O | 서버 발급 access token |
| tokenType | string | O | bearer |
| user | UserResponse | O | 사용자 정보 |

---

## 6. Usage Log Schema

### 6.1 UsageLogCreateRequest

Phase 1 개발 단계:

```json
{
  "userId": "test_user_001",
  "date": "2026-05-01",
  "packageName": "com.google.android.youtube",
  "appName": "YouTube",
  "usageSeconds": 5400,
  "openCount": 12
}
```

Phase 2 인증 적용 이후:

```json
{
  "date": "2026-05-01",
  "packageName": "com.google.android.youtube",
  "appName": "YouTube",
  "usageSeconds": 5400,
  "openCount": 12
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| userId | string | Phase 1만 | 개발 단계용 사용자 ID |
| date | string | O | 사용 날짜 |
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| usageSeconds | int | O | 사용 시간. 초 단위 |
| openCount | int | X | 앱 실행 횟수 |

---

### 6.2 UsageLogBulkCreateRequest

Phase 1 개발 단계:

```json
{
  "userId": "test_user_001",
  "logs": [
    {
      "date": "2026-05-01",
      "packageName": "com.google.android.youtube",
      "appName": "YouTube",
      "usageSeconds": 5400,
      "openCount": 12
    }
  ]
}
```

Phase 2 인증 적용 이후:

```json
{
  "logs": [
    {
      "date": "2026-05-01",
      "packageName": "com.google.android.youtube",
      "appName": "YouTube",
      "usageSeconds": 5400,
      "openCount": 12
    }
  ]
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| userId | string | Phase 1만 | 개발 단계용 사용자 ID |
| logs | UsageLogCreateItem[] | O | 사용 로그 목록 |

---

### 6.3 UsageLogCreateItem

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| date | string | O | 사용 날짜 |
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| usageSeconds | int | O | 사용 시간. 초 단위 |
| openCount | int | X | 앱 실행 횟수 |

---

### 6.4 UsageLogResponse

```json
{
  "usageLogId": "test_user_001_2026-05-01_com.google.android.youtube",
  "userId": "test_user_001",
  "date": "2026-05-01",
  "packageName": "com.google.android.youtube",
  "appName": "YouTube",
  "category": "ENTERTAINMENT",
  "usageSeconds": 5400,
  "openCount": 12
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| usageLogId | string | O | 사용 로그 ID |
| userId | string | O | 사용자 ID |
| date | string | O | 사용 날짜 |
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| category | string | O | 앱 카테고리 |
| usageSeconds | int | O | 사용 시간. 초 단위 |
| openCount | int | X | 앱 실행 횟수 |

---

### 6.5 UsageLogCreateResponse

```json
{
  "message": "usage log saved",
  "usageLog": {
    "usageLogId": "test_user_001_2026-05-01_com.google.android.youtube",
    "userId": "test_user_001",
    "date": "2026-05-01",
    "packageName": "com.google.android.youtube",
    "appName": "YouTube",
    "category": "ENTERTAINMENT",
    "usageSeconds": 5400,
    "openCount": 12
  }
}
```

---

### 6.6 UsageLogBulkCreateResponse

```json
{
  "message": "usage logs saved",
  "savedCount": 2
}
```

---

### 6.7 UsageLogListResponse

```json
{
  "date": "2026-05-01",
  "logs": [
    {
      "usageLogId": "test_user_001_2026-05-01_com.google.android.youtube",
      "userId": "test_user_001",
      "date": "2026-05-01",
      "packageName": "com.google.android.youtube",
      "appName": "YouTube",
      "category": "ENTERTAINMENT",
      "usageSeconds": 5400,
      "openCount": 12
    }
  ]
}
```

---

## 7. Summary Schema

### 7.1 TopAppUsageResponse

```json
{
  "packageName": "com.google.android.youtube",
  "appName": "YouTube",
  "category": "ENTERTAINMENT",
  "usageSeconds": 5400
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| category | string | O | 앱 카테고리 |
| usageSeconds | int | O | 사용 시간. 초 단위 |

---

### 7.2 CategoryUsageResponse

```json
{
  "category": "ENTERTAINMENT",
  "usageSeconds": 7800
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| category | string | O | 앱 카테고리 |
| usageSeconds | int | O | 사용 시간. 초 단위 |

---

### 7.3 DailySummaryResponse

```json
{
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
  ]
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| date | string | O | 요약 날짜 |
| totalUsageSeconds | int | O | 하루 총 사용 시간 |
| topApps | TopAppUsageResponse[] | O | 사용량 상위 앱 |
| categorySummaries | CategoryUsageResponse[] | O | 카테고리별 사용량 |

---

## 8. App Category Schema

### 8.1 AppCategoryResponse

```json
{
  "packageName": "com.google.android.youtube",
  "appName": "YouTube",
  "category": "ENTERTAINMENT",
  "isUserDefined": false
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| category | string | O | 앱 카테고리 |
| isUserDefined | boolean | O | 사용자 직접 수정 여부 |

---

### 8.2 AppCategoryListResponse

```json
{
  "categories": [
    {
      "packageName": "com.google.android.youtube",
      "appName": "YouTube",
      "category": "ENTERTAINMENT",
      "isUserDefined": false
    }
  ]
}
```

---

### 8.3 AppCategoryUpdateRequest

```json
{
  "appName": "YouTube",
  "category": "ENTERTAINMENT"
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| appName | string | O | 앱 표시 이름 |
| category | string | O | 변경할 카테고리 |

---

### 8.4 AppCategoryUpdateResponse

```json
{
  "message": "app category updated",
  "category": {
    "packageName": "com.google.android.youtube",
    "appName": "YouTube",
    "category": "ENTERTAINMENT",
    "isUserDefined": true
  }
}
```

---

## 9. Analysis Schema

### 9.1 DailyAnalysisRequest

Phase 1 개발 단계:

```json
{
  "userId": "test_user_001",
  "date": "2026-05-01"
}
```

Phase 2 인증 적용 이후:

```json
{
  "date": "2026-05-01"
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| userId | string | Phase 1만 | 개발 단계용 사용자 ID |
| date | string | O | 분석 날짜 |

---

### 9.2 DailyAnalysisResponse

```json
{
  "date": "2026-05-01",
  "totalUsageSeconds": 14400,
  "mainProblem": "ENTERTAINMENT",
  "insight": "오늘은 YouTube와 Webtoon 사용 시간이 길어 엔터테인먼트 앱 사용 비중이 높았습니다.",
  "recommendation": "내일은 엔터테인먼트 앱 사용 시간을 1시간 줄이는 것을 목표로 해보는 것이 좋습니다.",
  "topApps": [
    {
      "packageName": "com.google.android.youtube",
      "appName": "YouTube",
      "category": "ENTERTAINMENT",
      "usageSeconds": 5400
    }
  ]
}
```

### Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| date | string | O | 분석 날짜 |
| totalUsageSeconds | int | O | 하루 총 사용 시간 |
| mainProblem | string/null | X | 주요 문제 카테고리 |
| insight | string | O | AI 분석 문장 |
| recommendation | string | O | 행동 추천 문장 |
| topApps | TopAppUsageResponse[] | O | 사용량 상위 앱 |

---

## 10. 검증 규칙

### 10.1 UsageLogCreateRequest

```text
date는 YYYY-MM-DD 형식이어야 한다.
packageName은 빈 문자열이면 안 된다.
appName은 빈 문자열이면 안 된다.
usageSeconds는 0보다 커야 한다.
openCount는 0 이상이어야 한다.
category는 클라이언트가 보내지 않는다.
```

---

### 10.2 AppCategoryUpdateRequest

```text
appName은 빈 문자열이면 안 된다.
category는 정의된 enum 중 하나여야 한다.
```

---

### 10.3 DailyAnalysisRequest

```text
date는 YYYY-MM-DD 형식이어야 한다.
Phase 2에서는 userId를 body에 넣지 않는다.
```

---

## 11. 최종 결정 사항

```text
DB는 Firebase Firestore를 사용한다.
UsageLog는 세션 로그가 아니라 하루 앱별 요약 로그이다.
startTime/endTime은 MVP에서 사용하지 않는다.
minutesUsed는 사용하지 않는다.
usageSeconds를 사용한다.
API 경로는 /usage-logs 계열로 통일한다.
서버에는 영어 category enum 값을 저장한다.
Flutter 앱에서 한국어 라벨로 변환한다.
카테고리는 STUDY, PRODUCTIVITY, COMMUNICATION, ENTERTAINMENT, GAME, SNS, SYSTEM, ETC 총 8개를 사용한다.
```

---

## 현재 구현 메모

### UsageLog 요청

`UsageLogCreateRequest`와 `UsageLogCreateItem`에는 `category`를 포함하지 않는다.

클라이언트는 다음 값을 보낸다.

```json
{
  "date": "2026-05-01",
  "packageName": "com.google.android.youtube",
  "appName": "YouTube",
  "usageSeconds": 5400,
  "openCount": 12
}
```

서버는 분류를 마친 뒤 `UsageLogResponse`에 `category`를 포함해 반환한다.

### 카테고리 분류

유효한 카테고리는 다음 8개를 유지한다.

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

모르는 일반 앱은 OpenAI로 분류할 수 있다. AI 결과가 없거나 유효하지 않으면 반드시 `ETC`로 대체 분류한다.

### DailyAnalysis 응답

`DailyAnalysisResponse`는 OpenAI로 생성될 수 있다. 응답 형태는 그대로 유지한다.

```json
{
  "date": "2026-05-01",
  "totalUsageSeconds": 14400,
  "mainProblem": "ENTERTAINMENT",
  "insight": "...",
  "recommendation": "...",
  "topApps": []
}
```
