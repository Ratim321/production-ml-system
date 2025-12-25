"""Service for retrieving model metrics"""
from typing import Dict, Any, List
from datetime import datetime
from app.database import SessionLocal
from app.models import ModelMetrics, ModelVersion
from app.schemas import MetricsResponse


class MetricsService:
    """Service for model metrics"""
    
    def get_latest_metrics(self, model_version: str = None) -> MetricsResponse:
        """Get latest metrics for a model version"""
        db = SessionLocal()
        try:
            if model_version is None:
                # Get latest active model
                model = db.query(ModelVersion).filter(
                    ModelVersion.status == "active"
                ).first()
                if not model:
                    raise ValueError("No active model found")
                model_version = model.version
            
            # Get metrics
            metrics_records = db.query(ModelMetrics).filter(
                ModelMetrics.model_version == model_version
            ).all()
            
            metrics = {m.metric_name: m.metric_value for m in metrics_records}
            
            return MetricsResponse(
                model_version=model_version,
                metrics=metrics,
                timestamp=datetime.now()
            )
        finally:
            db.close()
    
    def get_all_model_versions(self) -> List[Dict[str, Any]]:
        """Get all model versions"""
        db = SessionLocal()
        try:
            models = db.query(ModelVersion).order_by(ModelVersion.created_at.desc()).all()
            return [
                {
                    "version": m.version,
                    "model_type": m.model_type,
                    "status": m.status,
                    "traffic_percent": m.traffic_percent,
                    "created_at": m.created_at.isoformat(),
                    "performance_metrics": m.performance_metrics
                }
                for m in models
            ]
        finally:
            db.close()


