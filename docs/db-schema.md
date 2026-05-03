# Firestore Database Schema

## 1. 목적

이 문서는 Quokkawai 백엔드에서 사용하는 Firestore 컬렉션 구조를 정의한다.

Quokkawai MVP는 Firebase Firestore를 데이터베이스로 사용한다.

---

## 2. 컬렉션 목록

```text
users
usage_logs
app_categories
daily_summaries
daily_analyses
```

---

## 3. users

### 3.1 설명

사용자 정보를 저장하는 컬렉션이다.

Google OAuth 로그인 이후 서버가 사용자를 생성하거나 조회한다.

---

### 3.2 Document Path

```text
users/{userId}
```

---

### 3.3 Document Example

```json
{
  "userId": "user_001",
  "provider": "google",
  "providerUserId": "google-sub-value",
  "email": "user@example.com",
  "nickname": "user nickname",
  "createdAt": "2026-05-01T12:00:00+09:00",
  "updatedAt": "2026-05-01T12:00:00+09:00"
}
```

---

### 3.4 Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| userId | string | O | 서버 내부 사용자 ID |
| provider | string | O | 로그인 제공자 |
| providerUserId | string | O | Google 계정 고유 ID |
| email | string/null | X | 사용자 이메일 |
| nickname | string/null | X | 사용자 표시 이름 |
| createdAt | datetime | O | 생성 시간 |
| updatedAt | datetime | O | 수정 시간 |

---

## 4. usage_logs

### 4.1 설명

사용자의 하루 앱별 사용량 요약 로그를 저장하는 컬렉션이다.

세션 단위 사용 기록이 아니라, 특정 날짜에 특정 앱을 총 몇 초 사용했는지를 저장한다.

---

### 4.2 Document Path

```text
usage_logs/{usageLogId}
```

권장 usageLogId 형식:

```text
{userId}_{date}_{packageName}
```

예시:

```text
user_001_2026-05-01_com.google.android.youtube
```

---

### 4.3 Document Example

```json
{
  "usageLogId": "user_001_2026-05-01_com.google.android.youtube",
  "userId": "user_001",
  "date": "2026-05-01",
  "packageName": "com.google.android.youtube",
  "appName": "YouTube",
  "category": "ENTERTAINMENT",
  "usageSeconds": 5400,
  "openCount": 12,
  "createdAt": "2026-05-01T23:30:00+09:00",
  "updatedAt": "2026-05-01T23:30:00+09:00"
}
```

---

### 4.4 Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| usageLogId | string | O | 사용 로그 ID |
| userId | string | O | 사용자 ID |
| date | string | O | 사용 날짜. YYYY-MM-DD |
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| category | string | O | 앱 카테고리 |
| usageSeconds | int | O | 사용 시간. 초 단위 |
| openCount | int | X | 앱 실행 횟수 |
| createdAt | datetime | O | 생성 시간 |
| updatedAt | datetime | O | 수정 시간 |

---

### 4.5 Query Pattern

특정 사용자의 특정 날짜 사용 로그 조회:

```text
where userId == {userId}
where date == {date}
```

특정 사용자의 기간별 사용 로그 조회:

```text
where userId == {userId}
where date >= {startDate}
where date <= {endDate}
```

---

### 4.6 설계 비고

같은 사용자, 같은 날짜, 같은 앱 패키지명에 대해서는 하나의 문서만 존재해야 한다.

따라서 동일한 usageLogId로 다시 저장하는 경우 새 문서를 추가하는 것이 아니라 기존 문서를 덮어쓰거나 업데이트한다.

---

## 5. app_categories

### 5.1 설명

앱 패키지명과 카테고리의 매핑 정보를 저장하는 컬렉션이다.

서버는 packageName을 기준으로 앱의 카테고리를 결정한다.

---

### 5.2 Document Path

```text
app_categories/{packageName}
```

예시:

```text
app_categories/com.google.android.youtube
```

---

### 5.3 Document Example

```json
{
  "packageName": "com.google.android.youtube",
  "appName": "YouTube",
  "category": "ENTERTAINMENT",
  "isUserDefined": false,
  "createdAt": "2026-05-01T12:00:00+09:00",
  "updatedAt": "2026-05-01T12:00:00+09:00"
}
```

---

### 5.4 Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| packageName | string | O | Android 앱 패키지명 |
| appName | string | O | 앱 표시 이름 |
| category | string | O | 앱 카테고리 |
| isUserDefined | boolean | O | 사용자가 직접 수정한 카테고리인지 여부 |
| createdAt | datetime | O | 생성 시간 |
| updatedAt | datetime | O | 수정 시간 |

---

### 5.5 Category Enum

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

### 5.6 기본 카테고리 예시

| packageName | appName | category |
|---|---|---|
| com.google.android.youtube | YouTube | ENTERTAINMENT |
| com.instagram.android | Instagram | SNS |
| com.nhn.android.webtoon | Naver Webtoon | ENTERTAINMENT |
| com.kakao.talk | KakaoTalk | COMMUNICATION |
| com.google.android.gm | Gmail | COMMUNICATION |
| com.google.android.calendar | Google Calendar | PRODUCTIVITY |
| com.android.settings | Settings | SYSTEM |

---

## 6. daily_summaries

### 6.1 설명

특정 사용자의 특정 날짜 사용 요약 결과를 저장하는 컬렉션이다.

MVP 초기에는 이 컬렉션을 생략하고 요청 시 `usage_logs`에서 즉시 계산할 수 있다.

---

### 6.2 Document Path

```text
daily_summaries/{userId}_{date}
```

예시:

```text
daily_summaries/user_001_2026-05-01
```

---

### 6.3 Document Example

```json
{
  "summaryId": "user_001_2026-05-01",
  "userId": "user_001",
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
  ],
  "createdAt": "2026-05-01T23:40:00+09:00",
  "updatedAt": "2026-05-01T23:40:00+09:00"
}
```

---

### 6.4 Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| summaryId | string | O | 요약 문서 ID |
| userId | string | O | 사용자 ID |
| date | string | O | 요약 날짜 |
| totalUsageSeconds | int | O | 하루 총 사용 시간 |
| topApps | array | O | 사용량 상위 앱 목록 |
| categorySummaries | array | O | 카테고리별 사용량 요약 |
| createdAt | datetime | O | 생성 시간 |
| updatedAt | datetime | O | 수정 시간 |

---

## 7. daily_analyses

### 7.1 설명

특정 사용자의 특정 날짜 AI 분석 결과를 저장하는 컬렉션이다.

---

### 7.2 Document Path

```text
daily_analyses/{userId}_{date}
```

예시:

```text
daily_analyses/user_001_2026-05-01
```

---

### 7.3 Document Example

```json
{
  "analysisId": "user_001_2026-05-01",
  "userId": "user_001",
  "date": "2026-05-01",
  "mainProblem": "ENTERTAINMENT",
  "insight": "오늘은 YouTube와 Webtoon 사용 시간이 길어 엔터테인먼트 앱 사용 비중이 높았습니다.",
  "recommendation": "내일은 엔터테인먼트 앱 사용 시간을 1시간 줄이는 것을 목표로 해보는 것이 좋습니다.",
  "createdAt": "2026-05-01T23:45:00+09:00",
  "updatedAt": "2026-05-01T23:45:00+09:00"
}
```

---

### 7.4 Fields

| 필드 | 타입 | 필수 | 설명 |
|---|---|---:|---|
| analysisId | string | O | AI 분석 문서 ID |
| userId | string | O | 사용자 ID |
| date | string | O | 분석 날짜 |
| mainProblem | string/null | X | 주요 문제 카테고리 |
| insight | string | O | AI 분석 문장 |
| recommendation | string | O | 행동 추천 문장 |
| createdAt | datetime | O | 생성 시간 |
| updatedAt | datetime | O | 수정 시간 |

---

## 8. 설계 원칙

### 8.1 userId 처리

초기 개발 단계에서는 요청 body 또는 query parameter에 userId를 포함할 수 있다.

Google 로그인 연동 이후에는 클라이언트가 userId를 직접 보내지 않고, 서버가 인증 토큰에서 userId를 추출한다.

---

### 8.2 시간 단위

사용 시간은 초 단위로 저장한다.

```text
usageSeconds
```

`minutesUsed`는 사용하지 않는다.

---

### 8.3 카테고리 저장 방식

서버와 DB에는 영어 enum 값을 저장한다.

Flutter 앱에서는 enum 값을 한국어 라벨로 변환하여 표시한다.

---

### 8.4 시스템 앱 처리

시스템 앱은 `SYSTEM`으로 분류하거나 분석 결과에서 제외할 수 있다.

예시:

```text
com.android.systemui
com.google.android.gms
com.google.android.inputmethod.latin
com.samsung.android.app.launcher
```

---

## 9. 인덱스 고려사항

Firestore에서 다음 조회가 자주 사용된다.

```text
usage_logs: userId + date
usage_logs: userId + date range
daily_summaries: userId + date
daily_analyses: userId + date
```

필요 시 Firebase Console에서 복합 인덱스를 생성한다.

---

## Current Implementation Notes

### app_categories Cache

The `app_categories` collection is used as a reusable category cache.

Category records can come from:

```text
default backend mapping
manual user update
OpenAI classification for unknown apps
SYSTEM prefix fallback
ETC fallback
```

Recommended document path remains:

```text
app_categories/{packageName}
```

If OpenAI classifies an unknown package, the backend should save:

```json
{
  "packageName": "com.example.app",
  "appName": "Example App",
  "category": "PRODUCTIVITY",
  "isUserDefined": false
}
```

Manual user updates should set `isUserDefined` to `true` and override future AI/default classification.
