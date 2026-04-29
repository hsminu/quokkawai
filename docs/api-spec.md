# API 명세서

## 1. 서버 상태 확인

### GET /

### Response

```json
{
  "message": "Quokkawai backend is running"
}
```

---

## 2. 사용 로그 업로드

### POST /upload-log

### Request

```json
{
  "appName": "YouTube",
  "packageName": "com.google.android.youtube",
  "minutesUsed": 43,
  "screenText": "자료구조 강의",
  "timeOfDay": "night"
}
```

### Response

```json
{
  "message": "log received",
  "data": {
    "appName": "YouTube",
    "packageName": "com.google.android.youtube",
    "minutesUsed": 43,
    "screenText": "자료구조 강의",
    "timeOfDay": "night"
  }
}
```

---

## 3. 일간 리포트 조회

### GET /daily-report/{user_id}

### Response

```json
{
  "userId": "user_001",
  "date": "2026-04-29",
  "totalMinutes": 312,
  "topApps": [
    {
      "appName": "YouTube",
      "minutesUsed": 92,
      "category": "엔터테인먼트"
    },
    {
      "appName": "Instagram",
      "minutesUsed": 74,
      "category": "쇼츠/도파민"
    }
  ],
  "oneLineFeedback": "오늘은 짧은 영상 소비 시간이 많았습니다."
}
```

---

## 4. 추후 추가 예정 API

### POST /analyze-usage

AI 기반 사용 패턴 분석 API.

### GET /stats/{user_id}

기간별 통계 조회 API.

### POST /auth/login

로그인 API.
