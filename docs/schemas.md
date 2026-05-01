# Quokkawai Backend DTO / Schema Spec

## 0. 목적

이 문서는 Quokkawai 백엔드와 Flutter 앱이 주고받는 요청/응답 데이터 형식을 정의한다.

DB 모델은 서버 내부 저장 구조이고, DTO는 API 통신용 데이터 구조이다.  
따라서 DB 컬럼명과 DTO 필드명이 반드시 1:1로 같을 필요는 없지만, 가능하면 일관성을 유지한다.

---

# 1. 공통 규칙

## 1.1 날짜/시간 형식

모든 시간 값은 ISO 8601 문자열을 사용한다.

```json
"2026-05-01T13:20:00"
```

서버 내부에서는 가능하면 timezone-aware datetime을 사용한다.

권장 기준:

```text
Asia/Seoul 기준으로 수집
서버 저장 시 UTC 또는 timezone-aware datetime으로 저장
응답 시 클라이언트가 이해 가능한 ISO 8601 문자열로 반환
```

---

## 1.2 필드 네이밍

API 요청/응답에서는 camelCase를 사용한다.

예시:

```json
{
  "packageName": "com.google.android.youtube",
  "usageSeconds": 1800
}
```

Python 내부 Pydantic 모델에서는 snake_case를 사용해도 된다.

예시:

```python
package_name: str
usage_seconds: int
```

단, FastAPI 응답에서는 alias를 사용해 camelCase로 내려주는 것을 권장한다.

---

## 1.3 공통 에러 응답

모든 API 에러 응답은 아래 형식을 따른다.

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid request body",
    "detail": "startTime must be earlier than endTime"
  }
}
```

### ErrorResponse

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| error | object | O | 에러 객체 |

### ErrorDetail

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| code | string | O | 에러 코드 |
| message | string | O | 사용자 또는 개발자가 이해할 수 있는 요약 메시지 |
| detail | string/null | X | 상세 설명 |

### 주요 에러 코드

| 코드 | 의미 |
|---|---|
| INVALID_REQUEST | 요청 형식이 잘못됨 |
| UNAUTHORIZED | 인증 실패 |
| FORBIDDEN | 권한 없음 |
| NOT_FOUND | 리소스를 찾을 수 없음 |
| CONFLICT | 중복 또는 충돌 발생 |
| INTERNAL_SERVER_ERROR | 서버 내부 오류 |

---

# 2. Auth DTO

현재는 Google OAuth 로그인만 지원한다고 가정한다.

앱에서 Google 로그인을 수행한 뒤, 서버에는 Google ID Token을 전달한다.  
서버는 해당 토큰을 검증하고 내부 userId를 발급하거나 기존 사용자를 조회한다.

---

## 2.1 Google 로그인 요청

### Endpoint

```http
POST /auth/google
```

### GoogleLoginRequest

```json
{
  "idToken": "google-id-token-value"
}
```

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| idToken | string | O | Google 로그인 후 발급받은 ID Token |

---

## 2.2 Google 로그인 응답

### GoogleLoginResponse

```json
{
  "accessToken": "server-access-token",
  "tokenType": "bearer",
  "user": {
    "userId": 1,
    "provider": "google",
    "providerUserId": "google-sub-value",
    "email": "user@example.com",
    "nickname": "기범"
  }
}
```

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| accessToken | string | O | 서버에서 발급한 인증 토큰 |
| tokenType | string | O | 일반적으로 bearer |
| user | object | O | 사용자 정보 |

### UserResponse

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| userId | int | O | 서버 내부 사용자 ID |
| provider | string | O | 로그인 제공자. 현재는 google |
| providerUserId | string | O | Google 계정 고유 ID |
| email | string/null | X | Google 계정 이메일 |
| nickname | string/null | X | 사용자 표시 이름 |

---

## 2.3 내 정보 조회

### Endpoint

```http
GET /auth/me
```

### Header

```http
Authorization: Bearer {accessToken}
```

### Response

```json
{
  "userId": 1,
  "provider": "google",
  "providerUserId": "google-sub-value",
  "email": "user@example.com",
  "nickname": "기범"
}
```

---

# 3. Usage Log DTO

Usage Log는 앱 사용 구간을 서버에 업로드하는 데이터이다.

예시:

```text
YouTube를 13:20부터 13:45까지 사용
Instagram을 14:00부터 14:10까지 사용
```

이런 이벤트성 사용 기록을 저장한다.

---

## 3.1 사용 로그 업로드 요청

### Endpoint

```http
POST /usage/logs
```

### Header

```http
Authorization: Bearer {accessToken}
```

### UsageLogCreateRequest

```json
{
  "packageName": "com.google.android.youtube",
  "appName": "YouTube",
  "startTime": "2026-05-01T13:20:00",
  "endTime": "2026-05-01T13:45:00"
}
```

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| startTime | datetime string | O | 사용 시작 시간 |
| endTime | datetime string | O | 사용 종료 시간 |

### 검증 규칙

```text
packageName은 빈 문자열이면 안 된다.
appName은 빈 문자열이면 안 된다.
startTime은 endTime보다 빨라야 한다.
usageSeconds = endTime - startTime으로 계산한다.
usageSeconds가 0 이하이면 저장하지 않는다.
```

---

## 3.2 사용 로그 업로드 응답

### UsageLogCreateResponse

```json
{
  "message": "usage log saved",
  "usageLogId": 101,
  "usageSeconds": 1500
}
```

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| message | string | O | 처리 결과 메시지 |
| usageLogId | int | O | 저장된 사용 로그 ID |
| usageSeconds | int | O | 계산된 사용 시간, 초 단위 |

---

## 3.3 사용 로그 목록 조회

### Endpoint

```http
GET /usage/logs?date=2026-05-01
```

### Header

```http
Authorization: Bearer {accessToken}
```

### Query Parameters

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| date | date string | O | 조회 날짜. YYYY-MM-DD |

### UsageLogListResponse

```json
{
  "date": "2026-05-01",
  "logs": [
    {
      "usageLogId": 101,
      "packageName": "com.google.android.youtube",
      "appName": "YouTube",
      "category": "ENTERTAINMENT",
      "startTime": "2026-05-01T13:20:00",
      "endTime": "2026-05-01T13:45:00",
      "usageSeconds": 1500
    }
  ]
}
```

### UsageLogResponse

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| usageLogId | int | O | 사용 로그 ID |
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| category | string/null | X | 앱 카테고리 |
| startTime | datetime string | O | 시작 시간 |
| endTime | datetime string | O | 종료 시간 |
| usageSeconds | int | O | 사용 시간, 초 단위 |

---

# 4. Daily Summary DTO

Daily Summary는 하루 단위 사용량 요약이다.

서버가 usage_logs를 기반으로 계산하거나, 추후 배치 작업으로 생성할 수 있다.

---

## 4.1 일일 요약 조회

### Endpoint

```http
GET /summary/daily?date=2026-05-01
```

### Header

```http
Authorization: Bearer {accessToken}
```

### DailySummaryResponse

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
    },
    {
      "packageName": "com.instagram.android",
      "appName": "Instagram",
      "category": "SNS",
      "usageSeconds": 3600
    },
    {
      "packageName": "com.nhn.android.webtoon",
      "appName": "Naver Webtoon",
      "category": "ENTERTAINMENT",
      "usageSeconds": 2400
    }
  ],
  "categorySummaries": [
    {
      "category": "ENTERTAINMENT",
      "usageSeconds": 7800
    },
    {
      "category": "SNS",
      "usageSeconds": 3600
    },
    {
      "category": "PRODUCTIVITY",
      "usageSeconds": 1800
    }
  ]
}
```

### DailySummaryResponse Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| date | date string | O | 요약 날짜 |
| totalUsageSeconds | int | O | 하루 전체 사용 시간 |
| topApps | array | O | 사용량 상위 앱 목록 |
| categorySummaries | array | O | 카테고리별 사용량 요약 |

### TopAppUsageResponse

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| category | string/null | X | 앱 카테고리 |
| usageSeconds | int | O | 사용 시간, 초 단위 |

### CategoryUsageResponse

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| category | string | O | 앱 카테고리 |
| usageSeconds | int | O | 사용 시간, 초 단위 |

---

# 5. App Category DTO

앱 카테고리는 앱 패키지명을 기준으로 관리한다.

초기에는 서버에서 기본 매핑을 갖고 있어도 되고,  
나중에는 AI가 앱 이름과 패키지명을 보고 자동 분류하도록 확장할 수 있다.

---

## 5.1 카테고리 enum

초기 카테고리는 아래 값만 사용한다.

```text
STUDY
PRODUCTIVITY
COMMUNICATION
INFORMATION_SEARCH
ENTERTAINMENT
SHORTS_DOPAMINE
GAME
SNS
SYSTEM
ETC
```

| 값 | 의미 |
|---|---|
| STUDY | 공부 |
| PRODUCTIVITY | 생산성 |
| COMMUNICATION | 커뮤니케이션 |
| INFORMATION_SEARCH | 정보검색 |
| ENTERTAINMENT | 엔터테인먼트 |
| SHORTS_DOPAMINE | 쇼츠/도파민 |
| GAME | 게임 |
| SNS | SNS |
| SYSTEM | 시스템 앱 |
| ETC | 기타 |

---

## 5.2 앱 카테고리 조회

### Endpoint

```http
GET /app-categories
```

### Header

```http
Authorization: Bearer {accessToken}
```

### AppCategoryListResponse

```json
{
  "categories": [
    {
      "packageName": "com.google.android.youtube",
      "appName": "YouTube",
      "category": "ENTERTAINMENT",
      "isUserDefined": false
    },
    {
      "packageName": "com.instagram.android",
      "appName": "Instagram",
      "category": "SNS",
      "isUserDefined": false
    }
  ]
}
```

### AppCategoryResponse

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| category | string | O | 앱 카테고리 |
| isUserDefined | boolean | O | 사용자가 직접 수정한 카테고리인지 여부 |

---

## 5.3 앱 카테고리 수정

### Endpoint

```http
PUT /app-categories/{packageName}
```

### Header

```http
Authorization: Bearer {accessToken}
```

### AppCategoryUpdateRequest

```json
{
  "appName": "YouTube",
  "category": "SHORTS_DOPAMINE"
}
```

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| appName | string | O | 앱 표시 이름 |
| category | string | O | 변경할 카테고리 |

### AppCategoryUpdateResponse

```json
{
  "message": "app category updated",
  "category": {
    "packageName": "com.google.android.youtube",
    "appName": "YouTube",
    "category": "SHORTS_DOPAMINE",
    "isUserDefined": true
  }
}
```

---

# 6. AI Analysis DTO

AI Analysis는 하루 사용량 요약을 바탕으로 한줄 피드백 또는 행동 분석을 생성한다.

초기 MVP에서는 다음 정도만 구현한다.

```text
오늘 총 사용 시간
상위 3개 앱
카테고리별 사용량
가장 과하게 사용한 앱
AI 한줄 피드백
```

---

## 6.1 AI 분석 요청

### Endpoint

```http
POST /analysis/daily
```

### Header

```http
Authorization: Bearer {accessToken}
```

### DailyAnalysisRequest

```json
{
  "date": "2026-05-01"
}
```

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| date | date string | O | 분석할 날짜 |

---

## 6.2 AI 분석 응답

### DailyAnalysisResponse

```json
{
  "date": "2026-05-01",
  "totalUsageSeconds": 14400,
  "mainProblem": "SHORTS_DOPAMINE",
  "insight": "오늘은 YouTube와 Instagram 사용 시간이 길어 짧은 자극성 콘텐츠에 시간이 많이 사용되었습니다.",
  "recommendation": "내일은 YouTube 사용 시간을 1시간 이내로 제한해보는 것이 좋습니다.",
  "topApps": [
    {
      "packageName": "com.google.android.youtube",
      "appName": "YouTube",
      "category": "SHORTS_DOPAMINE",
      "usageSeconds": 5400
    },
    {
      "packageName": "com.instagram.android",
      "appName": "Instagram",
      "category": "SNS",
      "usageSeconds": 3600
    },
    {
      "packageName": "com.nhn.android.webtoon",
      "appName": "Naver Webtoon",
      "category": "ENTERTAINMENT",
      "usageSeconds": 2400
    }
  ]
}
```

### DailyAnalysisResponse Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| date | date string | O | 분석 날짜 |
| totalUsageSeconds | int | O | 총 사용 시간 |
| mainProblem | string/null | X | 가장 문제가 되는 카테고리 또는 앱 |
| insight | string | O | AI 한줄 분석 |
| recommendation | string | O | 행동 추천 |
| topApps | array | O | 사용량 상위 앱 |

---

# 7. MVP에서 당장 필요한 API 우선순위

## 1순위

```text
POST /auth/google
GET /auth/me
POST /usage/logs
GET /usage/logs?date=
GET /summary/daily?date=
POST /analysis/daily
```

## 2순위

```text
GET /app-categories
PUT /app-categories/{packageName}
```

## 3순위

```text
GET /summary/weekly
GET /analysis/weekly
GET /statistics/rank
```

---

# 8. 백엔드 Pydantic 파일 구조 제안

```text
app/
  schemas/
    auth.py
    user.py
    usage.py
    summary.py
    app_category.py
    analysis.py
    common.py
```

---

# 9. 다음 구현 순서

## Step 1

Pydantic schema 작성

```text
schemas/common.py
schemas/user.py
schemas/auth.py
schemas/usage.py
schemas/summary.py
schemas/app_category.py
schemas/analysis.py
```

## Step 2

SQLAlchemy model 작성

```text
models/user.py
models/app_usage_log.py
models/app_category.py
```

## Step 3

Router 뼈대 작성

```text
routers/auth.py
routers/usage.py
routers/summary.py
routers/app_category.py
routers/analysis.py
```

## Step 4

Service 로직 작성

```text
services/auth_service.py
services/usage_service.py
services/summary_service.py
services/analysis_service.py
```

## Step 5

DB 연결 및 실행 테스트

```text
POST /usage/logs
GET /summary/daily?date=2026-05-01
POST /analysis/daily
```

---

# 10. 구현 시 주의사항

## 10.1 userId는 요청 body에 넣지 않는다

인증 이후에는 userId를 클라이언트가 직접 보내지 않는다.

나쁜 예:

```json
{
  "userId": 1,
  "packageName": "com.google.android.youtube"
}
```

좋은 예:

```http
Authorization: Bearer {accessToken}
```

서버가 토큰에서 userId를 알아낸다.

---

## 10.2 usageSeconds는 클라이언트가 보내지 않는다

사용 시간은 서버가 startTime, endTime으로 계산한다.

나쁜 예:

```json
{
  "usageSeconds": 1500
}
```

좋은 예:

```json
{
  "startTime": "2026-05-01T13:20:00",
  "endTime": "2026-05-01T13:45:00"
}
```

---

## 10.3 앱 카테고리는 서버에서 결정한다

클라이언트가 매번 category를 보내지 않는다.

서버가 packageName을 기준으로 카테고리를 결정한다.

```text
com.google.android.youtube -> ENTERTAINMENT 또는 SHORTS_DOPAMINE
com.instagram.android -> SNS
com.nhn.android.webtoon -> ENTERTAINMENT
```

---

## 10.4 시스템 앱 필터링 고려

초기에는 아래와 같은 시스템 앱은 분석에서 제외하거나 SYSTEM으로 분류한다.

```text
com.android.systemui
com.google.android.gms
com.google.android.inputmethod.latin
com.samsung.android.app.launcher
```

---

# 11. MVP 기준 최종 목표

MVP 백엔드는 다음 흐름이 가능해야 한다.

```text
1. 사용자가 Google 로그인
2. 앱이 사용 로그를 서버에 업로드
3. 서버가 사용 로그를 저장
4. 서버가 날짜별 사용량을 계산
5. 서버가 상위 사용 앱 3개를 반환
6. 서버가 카테고리별 사용량을 반환
7. 서버가 AI 한줄 분석을 반환
```

최소 성공 기준:

```text
오늘 YouTube 1시간 30분
Instagram 1시간
Webtoon 40분 사용

→ 총 사용 시간 3시간 10분
→ 상위 앱 3개 반환
→ 엔터테인먼트/SNS 중심 사용으로 분류
→ AI 피드백 한줄 생성
```
