"""Prediction API endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from app.schemas import (
    PredictionRequest, PredictionResponse,
    BatchPredictionRequest, BatchPredictionResponse
)
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/predict", tags=["predictions"])


@router.post("", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Real-time single prediction"""
    try:
        service = PredictionService()
        return service.predict_single(request.customer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """Batch prediction"""
    try:
        service = PredictionService()
        predictions = service.predict_batch(request.customers)
        return BatchPredictionResponse(
            predictions=predictions,
            total=len(predictions),
            model_version=predictions[0].model_version if predictions else "unknown"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


