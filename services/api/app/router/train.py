from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.domain.schemas import TrainStatus
from app.service.train_service import launch_training, get_status

router = APIRouter(prefix="/api/v1")


@router.post("/train", status_code=202)
async def start_training():
    launched = launch_training()
    if not launched:
        return JSONResponse(
            status_code=409,
            content={"detail": "Ya hay un entrenamiento en curso."},
        )
    return {"status": "running", "message": "Entrenamiento iniciado en background."}


@router.get("/train/status", response_model=TrainStatus)
async def training_status():
    return get_status()
