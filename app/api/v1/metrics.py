"""Metrics API endpoints"""
from fastapi import APIRouter, HTTPException
from app.schemas import MetricsResponse
from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=MetricsResponse)
async def get_metrics(model_version: str = None):
    """Get model performance metrics"""
    try:
        service = MetricsService()
        return service.get_latest_metrics(model_version)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


