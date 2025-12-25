"""SQLAlchemy database models"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Text
from sqlalchemy.sql import func
from app.database import Base


class Prediction(Base):
    """Prediction records"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    prediction = Column(Float)
    probability = Column(Float)
    model_version = Column(String)
    features = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_churn = Column(Boolean, nullable=True)  # Ground truth (if available)


class ModelMetrics(Base):
    """Model performance metrics"""
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String, index=True)
    metric_name = Column(String)
    metric_value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON)


class ModelVersion(Base):
    """Model version registry"""
    __tablename__ = "model_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, unique=True, index=True)
    model_type = Column(String)
    status = Column(String)  # active, canary, deprecated
    traffic_percent = Column(Integer, default=100)
    mlflow_run_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    performance_metrics = Column(JSON)


