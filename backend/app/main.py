from fastapi import FastAPI

from app.routers import analysis, app_categories, health, summary, usage_logs


# FastAPI 앱 진입점
app = FastAPI(title="Quokkawai API")

# MVP에서 사용할 라우터 등록
app.include_router(health.router)
app.include_router(usage_logs.router)
app.include_router(summary.router)
app.include_router(analysis.router)
app.include_router(app_categories.router)
