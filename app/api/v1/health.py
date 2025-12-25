"""Health check endpoints"""
from fastapi import APIRouter
from app.schemas import HealthResponse
from app.database import SessionLocal
from app.ml.model_manager import ModelManager
import mlflow
from app.config import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    # Check database
    db_status = "healthy"
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
    except Exception:
        db_status = "unhealthy"
    
    # Check MLflow
    mlflow_status = "healthy"
    try:
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        mlflow.search_experiments()
    except Exception:
        mlflow_status = "unhealthy"
    
    # Check model
    model_loaded = False
    try:
        manager = ModelManager()
        model_loaded = manager.current_model is not None
    except Exception:
        pass
    
    overall_status = "healthy" if all([
        db_status == "healthy",
        mlflow_status == "healthy",
        model_loaded
    ]) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        database=db_status,
        mlflow=mlflow_status,
        model_loaded=model_loaded
    )


