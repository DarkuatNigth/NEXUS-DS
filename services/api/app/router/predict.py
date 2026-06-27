from fastapi import APIRouter, HTTPException
from app.domain.schemas import PredictRequest, PredictResponse
from app.service.model_service import predict

router = APIRouter(prefix="/api/v1")


@router.post("/predict", response_model=PredictResponse)
async def predict_churn(request: PredictRequest):
    try:
        label, proba = predict(request.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return PredictResponse(churn=label, probability=round(proba, 4))
