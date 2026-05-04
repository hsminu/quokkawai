from fastapi import FastAPI

from app.routers.analysis import router as analysis_router
from app.routers.app_categories import router as app_categories_router
from app.routers.health import router as health_router
from app.routers.modes import router as modes_router
from app.routers.settings import router as settings_router
from app.routers.summary import router as summary_router
from app.routers.usage_logs import router as usage_logs_router


# FastAPI 앱 진입점
app = FastAPI(title="Quokkawai API")

# MVP에서 사용할 라우터 등록
app.include_router(health_router)
app.include_router(usage_logs_router)
app.include_router(summary_router)
app.include_router(analysis_router)
app.include_router(app_categories_router)
app.include_router(modes_router)
app.include_router(settings_router)
