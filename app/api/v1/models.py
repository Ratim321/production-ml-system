"""Model management API endpoints"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import ModelInfo
from app.services.metrics_service import MetricsService
from app.ml.model_manager import ModelManager

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=List[ModelInfo])
async def list_models():
    """List all model versions"""
    try:
        service = MetricsService()
        models = service.get_all_model_versions()
        return [ModelInfo(**m) for m in models]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{version}", response_model=ModelInfo)
async def get_model(version: str):
    """Get model details"""
    try:
        service = MetricsService()
        models = service.get_all_model_versions()
        model = next((m for m in models if m["version"] == version), None)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        return ModelInfo(**model)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info/current")
async def get_current_model_info():
    """Get current model information"""
    try:
        manager = ModelManager()
        return manager.get_model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


