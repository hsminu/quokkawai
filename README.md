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

## Current Backend MVP Notes

- FastAPI backend stores daily app usage logs through `/usage-logs`.
- Usage time is represented only as `usageSeconds`.
- The server decides app categories. Clients do not send `category`.
- Known apps use the server's local category mapping.
- Unknown non-system apps are classified with OpenAI once and cached in `app_categories`.
- If OpenAI is not configured or fails, unknown apps fall back to `ETC`.
- `/analysis/daily` uses OpenAI for insight/recommendation when available, with a local fallback.

## Environment Variables

Create `backend/.env` for local development:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.4-mini
```
