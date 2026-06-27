from fastapi import APIRouter, HTTPException
from app.domain.schemas import MetricsResponse
from app.repository.metrics_repository import load_metrics

router = APIRouter(prefix="/api/v1")


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    metrics = load_metrics()
    if metrics is None:
        raise HTTPException(
            status_code=404,
            detail="No hay métricas disponibles. Ejecuta POST /api/v1/train primero.",
        )
    return MetricsResponse(**metrics)
