"""Application configuration"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://mluser:mlpassword@localhost:5432/mldb"
    
    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "churn_prediction"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Model
    model_registry_path: str = "./models"
    default_model_version: str = "latest"
    
    # Feature Store
    feature_store_path: str = "./feature_store"
    
    # Canary Deployment
    canary_traffic_percent: int = 10
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()


