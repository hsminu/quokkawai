# API Specification

## 1. 목적

이 문서는 Quokkawai 백엔드 API의 엔드포인트, 요청 형식, 응답 형식을 정의한다.

백엔드는 FastAPI로 구현하고, 데이터베이스는 Firebase Firestore를 사용한다.

---

## 2. 공통 규칙

### 2.1 Base URL

개발 환경:

```text
http://localhost:8000
```

배포 환경 예시:

```text
https://api.quokkawai.com
```

---

### 2.2 인증 방식

최종 구현에서는 사용자 API 요청에 Authorization 헤더를 포함한다.

```http
Authorization: Bearer {accessToken}
```

단, 초기 개발 단계에서는 더미 userId를 요청 body 또는 query parameter에 포함하는 방식을 임시로 허용한다.

---

### 2.3 날짜 형식

날짜는 `YYYY-MM-DD` 형식을 사용한다.

예시:

```text
2026-05-01
```

---

### 2.4 시간 단위

앱 사용 시간은 초 단위로 표현한다.

```text
usageSeconds
```

`minutesUsed`는 사용하지 않는다.

---

### 2.5 카테고리 enum

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

## 3. Auth API

## 3.1 Google 로그인

### Endpoint

```http
POST /auth/google
```

### Description

Google ID Token을 서버에 전달하여 사용자를 로그인 처리한다.

서버는 Google ID Token을 검증하고, 기존 사용자를 조회하거나 신규 사용자를 생성한다.

---

### Request Body

```json
{
  "idToken": "google-id-token-value"
}
```

현재 구현은 Google ID Token을 검증한 뒤 서버 access token을 발급한다.
토큰 기반 API는 `Authorization: Bearer {accessToken}` 헤더에서 userId를 꺼내 쓴다.

---

### Response

```json
{
  "success": true,
  "accessToken": "server-access-token",
  "tokenType": "bearer",
  "user": {
    "userId": "google_google-sub-value",
    "provider": "google",
    "providerUserId": "google-sub-value",
    "email": "user@example.com",
    "nickname": "user nickname"
  }
}
```

---

## 3.2 내 정보 조회

### Endpoint

```http
GET /auth/me
```

### Header

```http
Authorization: Bearer {accessToken}
```

---

### Response

```json
{
  "userId": "user_001",
  "provider": "google",
  "providerUserId": "google-sub-value",
  "email": "user@example.com",
  "nickname": "user nickname"
}
```

---

## 4. Usage Logs API

## 4.1 사용 로그 단건 업로드

### Endpoint

```http
POST /usage-logs
```

### Description

특정 날짜의 앱별 사용량 요약 로그를 서버에 저장한다.

MVP에서는 세션 단위 로그가 아니라 하루 앱별 요약 로그를 사용한다.

---

### Request Body

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

---

### Response

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

## 4.2 사용 로그 벌크 업로드

### Endpoint

```http
POST /usage-logs/bulk
```

### Description

여러 개의 앱 사용량 요약 로그를 한 번에 서버에 저장한다.

Flutter 앱은 하루 사용량 수집 후 이 API를 사용하여 여러 앱의 사용량을 한 번에 업로드할 수 있다.

---

### Request Body

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
    },
    {
      "date": "2026-05-01",
      "packageName": "com.instagram.android",
      "appName": "Instagram",
      "usageSeconds": 3600,
      "openCount": 20
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
    },
    {
      "date": "2026-05-01",
      "packageName": "com.instagram.android",
      "appName": "Instagram",
      "usageSeconds": 3600,
      "openCount": 20
    }
  ]
}
```

---

### Response

```json
{
  "message": "usage logs saved",
  "savedCount": 2
}
```

---

## 4.3 특정 날짜 사용 로그 조회

### Endpoint

```http
GET /usage-logs?date=2026-05-01
```

### Header

```http
Authorization: Bearer {accessToken}
```

개발 단계에서는 query parameter로 userId를 임시 허용할 수 있다.

```http
GET /usage-logs?userId=test_user_001&date=2026-05-01
```

---

### Response

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
    },
    {
      "usageLogId": "test_user_001_2026-05-01_com.instagram.android",
      "userId": "test_user_001",
      "date": "2026-05-01",
      "packageName": "com.instagram.android",
      "appName": "Instagram",
      "category": "SNS",
      "usageSeconds": 3600,
      "openCount": 20
    }
  ]
}
```

---

## 5. Summary API

## 5.1 일일 사용 요약 조회

### Endpoint

```http
GET /summary/daily?date=2026-05-01
```

개발 단계에서는 userId를 임시 query parameter로 허용할 수 있다.

```http
GET /summary/daily?userId=test_user_001&date=2026-05-01
```

---

### Description

특정 날짜의 사용 로그를 기반으로 일일 사용 요약을 반환한다.

---

### Response

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

---

## 6. Analysis API

## 6.1 일일 AI 분석 요청

### Endpoint

```http
POST /analysis/daily
```

---

### Request Body

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

---

### Description

특정 날짜의 일일 사용 요약을 기반으로 AI 분석 결과를 생성한다.

서버는 먼저 사용 로그를 요약하고, 요약 데이터만 AI에 전달한다.

---

### Response

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

---

## 7. App Categories API

## 7.1 앱 카테고리 목록 조회

### Endpoint

```http
GET /app-categories
```

---

### Response

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

---

## 7.2 앱 카테고리 수정

### Endpoint

```http
PUT /app-categories/{packageName}
```

---

### Request Body

```json
{
  "appName": "YouTube",
  "category": "ENTERTAINMENT"
}
```

---

### Response

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

## 8. 공통 에러 응답

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid request body",
    "detail": "usageSeconds must be greater than 0"
  }
}
```

---

## 8.1 Error Code

| 코드 | 의미 |
|---|---|
| INVALID_REQUEST | 요청 형식 오류 |
| UNAUTHORIZED | 인증 실패 |
| FORBIDDEN | 권한 없음 |
| NOT_FOUND | 리소스를 찾을 수 없음 |
| CONFLICT | 중복 또는 충돌 |
| INTERNAL_SERVER_ERROR | 서버 내부 오류 |

---

## 현재 구현 메모

### 사용 로그 카테고리 결정

`POST /usage-logs`와 `POST /usage-logs/bulk`에서 클라이언트는 `category`를 보내지 않는다.

서버는 다음 순서로 `category`를 결정한다.

```text
1. packageName 기준 기존 앱 카테고리 매핑
2. 알려진 시스템 앱 package prefix 기준 SYSTEM 분류
3. 모르는 일반 앱에 대한 OpenAI 분류
4. OpenAI가 없거나 유효하지 않은 값을 반환하면 ETC 대체 분류
```

OpenAI가 모르는 앱을 성공적으로 분류하면 결과를 `app_categories`에 캐싱한다.

### 일일 분석

`POST /analysis/daily`는 저장된 사용 로그로 먼저 `DailySummary`를 만든다. OpenAI에는 원본 로그가 아니라 요약 데이터만 보낸다.

OpenAI 설정이 없거나 호출에 실패하면 서버는 로컬 대체 분석을 반환한다.

### OpenAI 환경 변수

백엔드는 `.env`에서 OpenAI 설정을 읽는다.

```env
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.4-mini
GOOGLE_CLIENT_ID=...
JWT_SECRET_KEY=...
JWT_EXPIRE_MINUTES=10080
```

### 사용자 설정 API

현재 설정은 앱별 제한이 아니라 목표 카테고리의 하루 총 사용 목표를 저장한다.
기본 목표 카테고리는 `SNS`, `GAME`, `ENTERTAINMENT`이다.

```http
GET /settings?userId=test_user_001
```

```http
PUT /settings?userId=test_user_001
Content-Type: application/json
```

```json
{
  "dailyUsageGoalMinutes": 240,
  "targetCategories": ["SNS", "GAME", "ENTERTAINMENT"],
  "analysisTone": "SOFT",
  "analysisSchedules": [
    {
      "scheduleId": "focus-1",
      "mode": "FOCUS",
      "title": "공부 시간",
      "startTime": "09:00",
      "endTime": "11:00",
      "enabled": true
    }
  ]
}
```

`analysisTone`은 `SOFT`, `FRIENDLY`, `DIRECT` 중 하나를 사용한다.
각각 부드러운 말투, 친한 친구 말투, 직설적인 말투로 AI 분석 문장을 생성한다.
`analysisSchedules`의 `FOCUS`와 `SLEEP`은 앱 차단용이 아니라 AI 분석 참고용 맥락이다.
`POST /analysis/daily`는 사용 로그 요약과 함께 이 사용자 설정을 읽어서 OpenAI 분석에 전달한다.

### 토큰 기반 API

로그인 응답의 `accessToken`은 다음 헤더로 보낸다.

```http
Authorization: Bearer {accessToken}
```

현재 추가된 토큰 기반 API는 다음과 같다.

```http
GET /auth/me
POST /usage-logs/me
POST /usage-logs/me/bulk
GET /usage-logs/me?date=2026-05-05
GET /settings/me
PUT /settings/me
POST /analysis/daily/me
```

`/usage-logs/me`, `/settings/me`, `/analysis/daily/me`는 요청 body나 query에서 `userId`를 받지 않고,
서버가 access token에서 검증된 userId를 꺼내 사용한다.
