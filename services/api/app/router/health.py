from fastapi import APIRouter
from app.service.health_service import check_health

router = APIRouter()


@router.get("/health")
async def health_check():
    return check_health()
