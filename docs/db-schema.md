# DB 스키마 초안

## 1. users

사용자 정보를 저장한다.

| 필드 | 타입 | 설명 |
|---|---|---|
| userId | string | 사용자 고유 ID |
| nickname | string | 닉네임 |
| createdAt | timestamp | 생성 시각 |

---

## 2. app_logs

앱 사용 로그를 저장한다.

| 필드 | 타입 | 설명 |
|---|---|---|
| logId | string | 로그 ID |
| userId | string | 사용자 ID |
| appName | string | 앱 이름 |
| packageName | string | 패키지명 |
| minutesUsed | number | 사용 시간 |
| screenText | string | 화면 텍스트 또는 사용 맥락 |
| timeOfDay | string | 사용 시간대 |
| category | string | AI 분류 카테고리 |
| createdAt | timestamp | 생성 시각 |

---

## 3. daily_reports

하루 단위 분석 결과를 저장한다.

| 필드 | 타입 | 설명 |
|---|---|---|
| reportId | string | 리포트 ID |
| userId | string | 사용자 ID |
| date | string | 날짜 |
| totalMinutes | number | 하루 총 사용시간 |
| topApps | array | 많이 사용한 앱 목록 |
| oneLineFeedback | string | AI 한줄 피드백 |
| createdAt | timestamp | 생성 시각 |

---

## 4. 카테고리 목록

| 카테고리 | 설명 |
|---|---|
| 공부 | 강의, 학습 자료, 문제 풀이 |
| 생산성 | 문서 작성, 일정 관리, 개발 |
| 커뮤니케이션 | 메신저, 이메일 |
| 정보검색 | 검색, 뉴스, 자료 조사 |
| 엔터테인먼트 | 영상, 음악, 웹툰 |
| 쇼츠/도파민 | 릴스, 쇼츠, 틱톡 등 짧은 콘텐츠 |
| 게임 | 모바일 게임 |
| 기타 | 분류 불가 |
