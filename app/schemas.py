"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CustomerFeatures(BaseModel):
    """Customer feature input for prediction"""
    customer_id: str
    age: int = Field(..., ge=0, le=120)
    tenure: int = Field(..., ge=0)
    monthly_charges: float = Field(..., ge=0)
    total_charges: float = Field(..., ge=0)
    contract_type: str = Field(..., pattern="^(Month-to-month|One year|Two year)$")
    payment_method: str
    paperless_billing: bool
    gender: str = Field(..., pattern="^(Male|Female)$")
    partner: bool
    dependents: bool
    phone_service: bool
    multiple_lines: bool
    internet_service: str
    online_security: bool
    online_backup: bool
    device_protection: bool
    tech_support: bool
    streaming_tv: bool
    streaming_movies: bool


class PredictionRequest(BaseModel):
    """Request for single prediction"""
    customer: CustomerFeatures


class BatchPredictionRequest(BaseModel):
    """Request for batch predictions"""
    customers: List[CustomerFeatures]


class PredictionResponse(BaseModel):
    """Prediction response"""
    customer_id: str
    prediction: float = Field(..., ge=0, le=1)
    probability: float = Field(..., ge=0, le=1)
    model_version: str
    timestamp: datetime


class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    predictions: List[PredictionResponse]
    total: int
    model_version: str


class ModelInfo(BaseModel):
    """Model information"""
    version: str
    model_type: str
    status: str
    traffic_percent: int
    created_at: datetime
    performance_metrics: Optional[Dict[str, Any]] = None


class MetricsResponse(BaseModel):
    """Metrics response"""
    model_version: str
    metrics: Dict[str, float]
    timestamp: datetime


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    database: str
    mlflow: str
    model_loaded: bool


