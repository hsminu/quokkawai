from fastapi import APIRouter


router = APIRouter(tags=["health"])


# 서버가 살아있는지 확인하는 간단한 체크
@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
