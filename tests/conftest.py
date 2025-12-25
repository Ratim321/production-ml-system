"""Pytest configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
import pandas as pd
from app.ml.trainer import ModelTrainer


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing"""
    return {
        "customer_id": "CUST_00001",
        "age": 45,
        "tenure": 12,
        "monthly_charges": 70.5,
        "total_charges": 846.0,
        "contract_type": "Month-to-month",
        "payment_method": "Electronic check",
        "paperless_billing": True,
        "gender": "Male",
        "partner": False,
        "dependents": False,
        "phone_service": True,
        "multiple_lines": False,
        "internet_service": "Fiber optic",
        "online_security": False,
        "online_backup": False,
        "device_protection": False,
        "tech_support": False,
        "streaming_tv": True,
        "streaming_movies": True
    }


@pytest.fixture
def sample_training_data():
    """Generate sample training data"""
    from scripts.generate_data import generate_customer_data
    return generate_customer_data(n_samples=100)


