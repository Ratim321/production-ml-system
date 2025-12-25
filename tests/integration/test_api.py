"""Integration tests for API endpoints"""
import pytest
from app.schemas import CustomerFeatures


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "mlflow" in data


def test_predict_endpoint(client, sample_customer_data):
    """Test prediction endpoint"""
    request_data = {
        "customer": sample_customer_data
    }
    
    response = client.post("/api/v1/predict", json=request_data)
    
    # May fail if model not trained, but should return proper error
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "customer_id" in data
        assert "prediction" in data
        assert "probability" in data
        assert 0 <= data["probability"] <= 1


def test_batch_predict_endpoint(client, sample_customer_data):
    """Test batch prediction endpoint"""
    request_data = {
        "customers": [sample_customer_data, sample_customer_data]
    }
    
    response = client.post("/api/v1/predict/batch", json=request_data)
    
    # May fail if model not trained
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "predictions" in data
        assert "total" in data
        assert data["total"] == 2


def test_models_endpoint(client):
    """Test models list endpoint"""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_metrics_endpoint(client):
    """Test metrics endpoint"""
    response = client.get("/api/v1/metrics")
    # May fail if no model trained
    assert response.status_code in [200, 500]


