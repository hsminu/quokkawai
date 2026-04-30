# API 명세서

## 1. 문서 목적

이 문서는 Quokkawai MVP의 프론트엔드와 백엔드 간 통신 규격을 정의한다.

프론트엔드는 이 문서의 API URL, Request JSON, Response JSON 형식에 맞춰 개발한다.  
백엔드는 이 문서의 응답 구조를 기준으로 FastAPI API를 구현한다.

---

## 2. 기본 정보

### Base URL

개발 환경에서는 아래 주소를 사용한다.

```text
http://127.0.0.1:8000
```

서버 배포 후에는 실제 서버 주소로 변경한다.

```text
https://api.quokkawai.com
```

---

## 3. 공통 규칙

### 날짜 형식

```text
YYYY-MM-DD
```

예시:

```text
2026-04-29
```

### 시간 형식

```text
HH:mm
```

예시:

```text
09:00
```

### datetime 형식

```text
ISO 8601
```

예시:

```text
2026-04-29T23:59:00
```

---

## 4. 공통 에러 응답

API 요청 실패 시 아래 형식을 사용한다.

```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "사용자를 찾을 수 없습니다."
  }
}
```

### 주요 에러 코드

| 코드 | 의미 |
|---|---|
| INVALID_REQUEST | 요청 형식이 잘못됨 |
| USER_NOT_FOUND | 사용자를 찾을 수 없음 |
| SETTINGS_NOT_FOUND | 사용자 설정을 찾을 수 없음 |
| REPORT_NOT_FOUND | 리포트를 찾을 수 없음 |
| GOOGLE_AUTH_FAILED | 구글 로그인 인증 실패 |
| INTERNAL_SERVER_ERROR | 서버 내부 오류 |

---

## 5. 인증 방식

MVP에서는 구글 로그인만 사용한다.

초기 개발 단계에서는 `userId`를 path 또는 body에 직접 포함해서 API를 호출한다.  
추후 Google 로그인과 JWT 인증을 연결한 뒤에는 `Authorization` 헤더를 사용한다.

### 추후 인증 헤더 형식

```http
Authorization: Bearer {accessToken}
```

---

# 6. Health Check API

## 6.1 서버 상태 확인

### Endpoint

```http
GET /
```

### 설명

백엔드 서버가 정상 실행 중인지 확인한다.

### Response

```json
{
  "success": true,
  "message": "Quokkawai backend is running"
}
```

---

# 7. Auth API

## 7.1 구글 로그인

### Endpoint

```http
POST /auth/google
```

### 설명

프론트에서 구글 로그인에 성공한 뒤 받은 구글 ID 토큰을 백엔드로 전달한다.  
백엔드는 해당 토큰을 검증하고, 기존 사용자가 있으면 로그인 처리하고 없으면 신규 사용자를 생성한다.

### Request

```json
{
  "idToken": "google_id_token_here"
}
```

### Response

```json
{
  "success": true,
  "accessToken": "app_access_token_here",
  "user": {
    "userId": "user_001",
    "googleUserId": "109238471928374",
    "email": "quokka@gmail.com",
    "name": "강현욱",
    "profileImageUrl": "https://example.com/profile.png",
    "createdAt": "2026-04-29T12:00:00",
    "updatedAt": "2026-04-29T12:00:00",
    "lastLoginAt": "2026-04-30T09:00:00"
  }
}
```

### 비고

초기 더미 백엔드에서는 실제 구글 토큰 검증 없이 임시 사용자 정보를 반환할 수 있다.  
실제 구현 단계에서는 반드시 구글 ID 토큰 검증을 수행해야 한다.

---

# 8. User API

## 8.1 내 정보 조회

### Endpoint

```http
GET /users/me
```

### 설명

현재 로그인한 사용자의 정보를 조회한다.

초기 개발 단계에서는 더미 유저 `user_001`을 반환한다.  
JWT 인증 연결 후에는 토큰에서 사용자 정보를 추출한다.

### Response

```json
{
  "success": true,
  "user": {
    "userId": "user_001",
    "googleUserId": "109238471928374",
    "email": "quokka@gmail.com",
    "name": "강현욱",
    "profileImageUrl": "https://example.com/profile.png",
    "createdAt": "2026-04-29T12:00:00",
    "updatedAt": "2026-04-29T12:00:00",
    "lastLoginAt": "2026-04-30T09:00:00"
  }
}
```

---

# 9. User Settings API

## 9.1 사용자 설정 조회

### Endpoint

```http
GET /users/{user_id}/settings
```

### 설명

사용자의 목표 설정 정보를 조회한다.  
목표 설정 화면에서 사용한다.

### Path Parameter

| 이름 | 타입 | 설명 |
|---|---|---|
| user_id | string | 사용자 ID |

### Example

```http
GET /users/user_001/settings
```

### Response

```json
{
  "success": true,
  "settings": {
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
}
```

---

## 9.2 사용자 설정 저장/수정

### Endpoint

```http
PUT /users/{user_id}/settings
```

### 설명

사용자의 목표 설정 정보를 저장하거나 수정한다.

### Path Parameter

| 이름 | 타입 | 설명 |
|---|---|---|
| user_id | string | 사용자 ID |

### Request

```json
{
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
  ]
}
```

### Response

```json
{
  "success": true,
  "message": "사용자 설정이 저장되었습니다.",
  "settings": {
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
}
```

---

# 10. Usage Log API

## 10.1 사용 로그 단일 업로드

### Endpoint

```http
POST /usage-logs
```

### 설명

Android에서 수집한 앱 사용 로그 1개를 서버에 업로드한다.

### Request

```json
{
  "userId": "user_001",
  "date": "2026-04-29",
  "appName": "YouTube",
  "packageName": "com.google.android.youtube",
  "category": "엔터테인먼트",
  "minutesUsed": 92,
  "openCount": 12,
  "notificationCount": 30,
  "timeOfDay": "night"
}
```

### Response

```json
{
  "success": true,
  "message": "사용 로그가 저장되었습니다.",
  "log": {
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
}
```

---

## 10.2 사용 로그 대량 업로드

### Endpoint

```http
POST /usage-logs/bulk
```

### 설명

Android에서 수집한 하루치 또는 일정 기간의 앱 사용 로그를 한 번에 서버에 업로드한다.

### Request

```json
{
  "userId": "user_001",
  "logs": [
    {
      "date": "2026-04-29",
      "appName": "YouTube",
      "packageName": "com.google.android.youtube",
      "category": "엔터테인먼트",
      "minutesUsed": 92,
      "openCount": 12,
      "notificationCount": 30,
      "timeOfDay": "night"
    },
    {
      "date": "2026-04-29",
      "appName": "Instagram",
      "packageName": "com.instagram.android",
      "category": "소셜 미디어",
      "minutesUsed": 74,
      "openCount": 18,
      "notificationCount": 25,
      "timeOfDay": "night"
    }
  ]
}
```

### Response

```json
{
  "success": true,
  "message": "사용 로그가 대량 저장되었습니다.",
  "savedCount": 2
}
```

---

## 10.3 일간 사용 로그 조회

### Endpoint

```http
GET /usage-logs/daily/{user_id}?date={date}
```

### 설명

특정 사용자의 특정 날짜 앱 사용 로그를 조회한다.

### Path Parameter

| 이름 | 타입 | 설명 |
|---|---|---|
| user_id | string | 사용자 ID |

### Query Parameter

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| date | string | O | 조회 날짜 |

### Example

```http
GET /usage-logs/daily/user_001?date=2026-04-29
```

### Response

```json
{
  "success": true,
  "userId": "user_001",
  "date": "2026-04-29",
  "logs": [
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
    },
    {
      "logId": "log_002",
      "userId": "user_001",
      "date": "2026-04-29",
      "appName": "Instagram",
      "packageName": "com.instagram.android",
      "category": "소셜 미디어",
      "minutesUsed": 74,
      "openCount": 18,
      "notificationCount": 25,
      "timeOfDay": "night",
      "createdAt": "2026-04-29T23:59:00"
    }
  ]
}
```

---

# 11. Report API

## 11.1 홈 화면 리포트 조회

### Endpoint

```http
GET /reports/home/{user_id}?date={date}
```

### 설명

홈 화면에 필요한 하루 요약 데이터를 조회한다.

### Path Parameter

| 이름 | 타입 | 설명 |
|---|---|---|
| user_id | string | 사용자 ID |

### Query Parameter

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| date | string | X | 조회 날짜. 없으면 오늘 날짜 사용 |

### Example

```http
GET /reports/home/user_001?date=2026-04-29
```

### Response

```json
{
  "success": true,
  "user": {
    "userId": "user_001",
    "name": "강현욱",
    "profileImageUrl": "https://example.com/profile.png"
  },
  "report": {
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
}
```

---

## 11.2 7일 분석 리포트 조회

### Endpoint

```http
GET /reports/weekly/{user_id}?startDate={startDate}&endDate={endDate}
```

### 설명

7일 분석 화면에 필요한 주간 요약 데이터를 조회한다.

### Path Parameter

| 이름 | 타입 | 설명 |
|---|---|---|
| user_id | string | 사용자 ID |

### Query Parameter

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| startDate | string | X | 시작 날짜. 없으면 최근 7일 기준 |
| endDate | string | X | 종료 날짜. 없으면 오늘 기준 |

### Example

```http
GET /reports/weekly/user_001?startDate=2026-04-23&endDate=2026-04-29
```

### Response

```json
{
  "success": true,
  "report": {
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
      },
      {
        "day": "수",
        "date": "2026-04-25",
        "minutes": 290
      },
      {
        "day": "목",
        "date": "2026-04-26",
        "minutes": 420
      },
      {
        "day": "금",
        "date": "2026-04-27",
        "minutes": 360
      },
      {
        "day": "토",
        "date": "2026-04-28",
        "minutes": 390
      },
      {
        "day": "일",
        "date": "2026-04-29",
        "minutes": 330
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
}
```

---

# 12. AI Coaching API

## 12.1 AI 코칭 리포트 생성

### Endpoint

```http
POST /ai/coaching-report
```

### 설명

사용자의 사용 로그와 주간 리포트를 기반으로 AI 코칭 리포트를 생성한다.

초기 개발 단계에서는 더미 리포트를 반환한다.  
이후 OpenAI API를 연결하여 실제 코칭 메시지와 추천 활동을 생성한다.

### Request

```json
{
  "userId": "user_001",
  "startDate": "2026-04-23",
  "endDate": "2026-04-29"
}
```

### Response

```json
{
  "success": true,
  "message": "AI 코칭 리포트가 생성되었습니다.",
  "report": {
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
      },
      {
        "day": "수",
        "date": "2026-04-25",
        "minutes": 260
      },
      {
        "day": "목",
        "date": "2026-04-26",
        "minutes": 350
      },
      {
        "day": "금",
        "date": "2026-04-27",
        "minutes": 290
      },
      {
        "day": "토",
        "date": "2026-04-28",
        "minutes": 270
      },
      {
        "day": "일",
        "date": "2026-04-29",
        "minutes": 240
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
}
```

---

## 12.2 AI 코칭 리포트 조회

### Endpoint

```http
GET /ai/coaching-report/{user_id}?startDate={startDate}&endDate={endDate}
```

### 설명

이미 생성된 AI 코칭 리포트를 조회한다.

### Path Parameter

| 이름 | 타입 | 설명 |
|---|---|---|
| user_id | string | 사용자 ID |

### Query Parameter

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| startDate | string | X | 시작 날짜 |
| endDate | string | X | 종료 날짜 |

### Example

```http
GET /ai/coaching-report/user_001?startDate=2026-04-23&endDate=2026-04-29
```

### Response

```json
{
  "success": true,
  "report": {
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
      },
      {
        "day": "수",
        "date": "2026-04-25",
        "minutes": 260
      },
      {
        "day": "목",
        "date": "2026-04-26",
        "minutes": 350
      },
      {
        "day": "금",
        "date": "2026-04-27",
        "minutes": 290
      },
      {
        "day": "토",
        "date": "2026-04-28",
        "minutes": 270
      },
      {
        "day": "일",
        "date": "2026-04-29",
        "minutes": 240
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
}
```

---

# 13. Category API

## 13.1 카테고리 목록 조회

### Endpoint

```http
GET /categories
```

### 설명

프론트와 백엔드가 동일한 카테고리 목록을 사용하기 위해 카테고리 목록을 조회한다.

### Response

```json
{
  "success": true,
  "categories": [
    "공부",
    "생산성",
    "커뮤니케이션",
    "정보검색",
    "소셜 미디어",
    "엔터테인먼트",
    "쇼츠/도파민",
    "게임",
    "기타"
  ]
}
```

---

# 14. MVP에서 구현하지 않는 API

아래 API는 MVP에서 구현하지 않는다.

```text
POST /auth/email/signup
POST /auth/email/login
POST /auth/kakao
POST /auth/apple

GET /friends
POST /friends
GET /rankings

GET /subscriptions
POST /subscriptions

GET /notifications
POST /notifications/push

GET /customer-support
POST /customer-support
```

프론트 화면에 관련 항목이 있어도 초기 단계에서는 더미 데이터 또는 비활성 버튼으로 처리한다.

---

# 15. MVP API 최종 목록

Quokkawai MVP에서 구현할 API는 다음과 같다.

```text
GET  /

POST /auth/google
GET  /users/me

GET  /users/{user_id}/settings
PUT  /users/{user_id}/settings

POST /usage-logs
POST /usage-logs/bulk
GET  /usage-logs/daily/{user_id}

GET  /reports/home/{user_id}
GET  /reports/weekly/{user_id}

POST /ai/coaching-report
GET  /ai/coaching-report/{user_id}

GET  /categories
```

---

# 16. 개발 우선순위

## 1순위

프론트 화면 연결을 위해 더미 데이터 기반으로 먼저 구현한다.

```text
GET /
GET /users/me
GET /users/{user_id}/settings
PUT /users/{user_id}/settings
GET /reports/home/{user_id}
GET /reports/weekly/{user_id}
GET /ai/coaching-report/{user_id}
GET /categories
```

## 2순위

Android 사용 로그 수집 기능과 연결한다.

```text
POST /usage-logs
POST /usage-logs/bulk
GET /usage-logs/daily/{user_id}
```

## 3순위

실제 구글 로그인과 AI 코칭 생성을 연결한다.

```text
POST /auth/google
POST /ai/coaching-report
```

---

# 17. 최종 결정

초기 백엔드는 실제 DB와 AI를 바로 붙이지 않는다.

먼저 더미 데이터 기반 API 서버를 구현하고, 프론트 화면이 정상적으로 API를 호출할 수 있도록 응답 형식을 고정한다.

그 후 순서대로 다음 기능을 붙인다.

```text
1. 더미 데이터 API 구현
2. Firebase 또는 DB 연결
3. Android 사용 로그 저장
4. Google 로그인 검증
5. OpenAI 기반 AI 코칭 생성
```
