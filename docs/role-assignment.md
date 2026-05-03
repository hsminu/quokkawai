# Role Assignment

## 1. 목적

이 문서는 Quokkawai 프로젝트의 팀원별 역할과 책임 범위를 정의한다.

역할 분담의 목적은 개발 충돌을 줄이고, 각 담당자가 책임져야 할 산출물을 명확히 하는 것이다.

---

## 2. 팀원 역할 개요

| 담당자 | 주요 역할 |
|---|---|
| 팀원 A | 백엔드 서버 구조, 사용 로그 API |
| 팀원 B | Flutter UI, 화면 구성 |
| 팀원 C | Android 사용량 수집, 권한 처리 |
| 팀원 D | 인증, 배포, API 연동 |
| 팀원 E | AI 분석, 데이터 시각화, 발표 자료 |

---

## 3. 팀원 A 역할

### 3.1 담당 영역

```text
FastAPI 백엔드 구조 설계
사용 로그 저장 API 구현
일일 요약 API 구현
Firestore 연동 코드 작성
API 명세 관리
```

### 3.2 주요 산출물

```text
FastAPI 프로젝트 기본 구조
사용 로그 저장 로직
사용 로그 조회 로직
일일 사용 요약 계산 로직
API 명세 문서
DTO / Schema 문서
```

### 3.3 구현 대상 API

```text
POST /usage-logs
POST /usage-logs/bulk
GET /usage-logs?date=
GET /summary/daily?date=
```

---

## 4. 팀원 B 역할

### 4.1 담당 영역

```text
Flutter 앱 화면 구성
로그인 화면 구현
메인 대시보드 구현
일일 리포트 화면 구현
AI 피드백 화면 구현
```

### 4.2 주요 산출물

```text
로그인 화면
홈 화면
일일 사용 요약 화면
AI 피드백 화면
앱별 사용량 리스트 화면
카테고리별 사용량 화면
```

### 4.3 구현 대상 화면

```text
로그인 화면
메인 대시보드
일일 사용 요약 화면
앱별 사용량 리스트
카테고리별 사용량 화면
AI 피드백 카드
```

---

## 5. 팀원 C 역할

### 5.1 담당 영역

```text
Android 앱 사용량 수집
사용량 접근 권한 요청 처리
앱별 사용 시간 계산
앱 실행 횟수 계산
백엔드 업로드용 데이터 변환
```

### 5.2 주요 산출물

```text
Android 사용량 수집 모듈
권한 요청 화면 또는 안내 로직
앱별 사용량 집계 로직
사용 로그 업로드 데이터 생성 코드
```

### 5.3 구현 대상 기능

```text
사용량 접근 권한 확인
사용량 접근 권한 요청 안내
오늘 날짜 앱 사용량 조회
앱별 usageSeconds 계산
앱별 openCount 계산
```

---

## 6. 팀원 D 역할

### 6.1 담당 영역

```text
Google OAuth 연동
서버 인증 흐름 설계
토큰 전달 방식 구현
서버 배포 환경 구성
프론트-백엔드 API 연동 테스트
```

### 6.2 주요 산출물

```text
Google 로그인 연동 코드
인증 토큰 전달 방식 정리
배포 환경 설정
API 연동 테스트 결과
```

### 6.3 구현 대상 API

```text
POST /auth/google
GET /auth/me
```

---

## 7. 팀원 E 역할

### 7.1 담당 영역

```text
AI 분석 프롬프트 설계
OpenAI API 연동 보조
카테고리별 사용량 시각화
발표용 더미 데이터 구성
발표 자료 기술 구조 정리
```

### 7.2 주요 산출물

```text
AI 피드백 프롬프트
AI 분석 응답 형식
카테고리별 사용량 그래프
발표용 시연 데이터
프로젝트 발표 자료
```

### 7.3 구현 대상 기능

```text
POST /analysis/daily
AI 피드백 문장 생성
카테고리별 사용량 차트
발표용 시연 시나리오
```

---

## 8. 공통 책임

모든 팀원은 다음 사항을 공통으로 지킨다.

```text
API 명세 변경 시 문서를 먼저 수정한다.
필드 이름은 문서 기준을 따른다.
카테고리 enum 값은 서버 기준 영어 값을 사용한다.
기능 구현 후 최소 1개 이상의 테스트 데이터를 남긴다.
```

---

## 9. 개발 우선순위

### 9.1 1차 목표

```text
더미 사용자 기준 사용 로그 저장
일일 요약 조회
Flutter 화면에서 결과 표시
```

### 9.2 2차 목표

```text
Google 로그인 연동
사용자별 데이터 분리
AI 피드백 생성
```

### 9.3 3차 목표

```text
배포
발표용 더미 데이터 구성
시연 시나리오 작성
```

---

## 10. 협업 규칙

```text
main 브랜치에 직접 push하지 않는다.
기능 단위로 브랜치를 나눈다.
API 변경은 docs/api-spec.md를 먼저 수정한다.
요청/응답 필드 변경은 docs/schemas.md를 먼저 수정한다.
DB 구조 변경은 docs/db-schema.md를 먼저 수정한다.
```

---

## 11. 브랜치 예시

```text
feature/backend-usage-logs
feature/backend-analysis
feature/flutter-dashboard
feature/android-usage-collector
feature/google-login
feature/deploy
```

---

## Current Implementation Notes

### Backend / AI Responsibility

The current backend MVP includes two AI-backed features:

```text
1. Daily usage analysis through POST /analysis/daily
2. Unknown app category classification during usage log save
```

Backend work owns the API flow, fallback behavior, and category cache writes.

AI work owns prompt quality, response format, and future improvement of analysis/category classification accuracy.

### Work Rule

OpenAI API keys must not be committed.

Local development uses:

```text
backend/.env
```

Only `backend/.env.example` should be committed.
