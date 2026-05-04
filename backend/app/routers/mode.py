from fastapi import APIRouter

from app.schemas.mode import ModeListResponse
from app.services.mode_service import get_mode_presets

router = APIRouter(
    prefix="/modes",
    tags=["Modes"]
)


@router.get("", response_model=ModeListResponse, summary="디톡스 모드 프리셋 목록 조회")
def read_mode_presets():
    """
    사용자에게 제공할 초급/중급/고급 디톡스 모드 설정 프리셋 목록을 반환합니다.
    """
    presets = get_mode_presets()
    return ModeListResponse(presets=presets)