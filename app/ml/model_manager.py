"""Model manager for loading and serving models"""
import os
import mlflow
import mlflow.sklearn
import joblib
from typing import Optional, Dict, Any
import numpy as np
from app.config import settings
from app.database import SessionLocal
from app.models import ModelVersion
from app.feature_store.transformer import FeatureTransformer


class ModelManager:
    """Manages model loading, versioning, and inference"""
    
    def __init__(self):
        self.current_model = None
        self.canary_model = None
        self.model_version = None
        self.canary_version = None
        self.feature_transformer = FeatureTransformer()
        self._load_models()
    
    def _load_models(self):
        """Load active and canary models"""
        db = SessionLocal()
        try:
            # Load active model
            active_model = db.query(ModelVersion).filter(
                ModelVersion.status == "active"
            ).first()
            
            if active_model:
                self.model_version = active_model.version
                try:
                    self.current_model = self._load_model_from_mlflow(active_model.mlflow_run_id)
                except Exception as e:
                    # Fallback to local file
                    print(f"Failed to load from MLflow: {e}. Trying local file...")
                    self.current_model = self._load_model_from_file(active_model.version)
            
            # Load canary model
            canary_model = db.query(ModelVersion).filter(
                ModelVersion.status == "canary"
            ).first()
            
            if canary_model:
                self.canary_version = canary_model.version
                try:
                    self.canary_model = self._load_model_from_mlflow(canary_model.mlflow_run_id)
                except Exception as e:
                    # Fallback to local file
                    print(f"Failed to load canary from MLflow: {e}. Trying local file...")
                    self.canary_model = self._load_model_from_file(canary_model.version)
        finally:
            db.close()
    
    def _load_model_from_mlflow(self, run_id: str):
        """Load model from MLflow"""
        try:
            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
            model_uri = f"runs:/{run_id}/model"
            return mlflow.sklearn.load_model(model_uri)
        except Exception as e:
            raise ValueError(f"Failed to load model from MLflow: {e}")
    
    def _load_model_from_file(self, version: str):
        """Load model from local file"""
        model_path = os.path.join(settings.model_registry_path, f"model_{version}.joblib")
        if os.path.exists(model_path):
            return joblib.load(model_path)
        return None
    
    def predict(self, features: np.ndarray, use_canary: bool = False) -> tuple:
        """Make prediction"""
        model = self.canary_model if use_canary and self.canary_model else self.current_model
        
        if model is None:
            raise ValueError("No model loaded")
        
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
        
        return float(prediction), float(probability)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        return {
            "active_version": self.model_version,
            "canary_version": self.canary_version,
            "has_active": self.current_model is not None,
            "has_canary": self.canary_model is not None
        }

