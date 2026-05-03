# Quokkawai

AI 기반 디지털 디톡스 앱 프로젝트입니다.

## 핵심 기능

- 앱 사용시간 수집
- 앱별 사용량 통계
- AI 기반 사용 패턴 분석
- 일간 리포트 제공

## 기술 스택

- Flutter
- FastAPI
- Firebase
- OpenAI API

## 현재 백엔드 MVP 메모

- FastAPI 백엔드는 `/usage-logs`로 하루 앱 사용 로그를 저장한다.
- 사용 시간은 `usageSeconds`만 사용한다.
- 앱 카테고리는 서버가 결정하며, 클라이언트는 `category`를 보내지 않는다.
- 이미 알고 있는 앱은 서버의 기본 카테고리 매핑을 사용한다.
- 모르는 일반 앱은 OpenAI로 한 번 분류하고 `app_categories`에 캐싱한다.
- OpenAI 설정이 없거나 호출에 실패하면 모르는 앱은 `ETC`로 분류한다.
- `/analysis/daily`는 가능하면 OpenAI로 `insight`와 `recommendation`을 만들고, 실패하면 로컬 대체 분석을 사용한다.

## 환경 변수

로컬 개발에서는 `backend/.env` 파일을 만든다.

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.4-mini
```
