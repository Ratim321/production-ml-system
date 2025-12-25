# System Architecture

## Overview

This is a production-ready machine learning system for customer churn prediction with the following components:

## Components

### 1. Data Pipeline (`scripts/generate_data.py`)
- Generates synthetic customer data
- Handles data preprocessing
- Creates training/test splits

### 2. Feature Store (`app/feature_store/`)
- Consistent feature engineering
- Transformers for encoding and scaling
- Reusable across training and inference

### 3. ML Training (`app/ml/trainer.py`)
- Model training with scikit-learn
- MLflow integration for experiment tracking
- Model versioning and registry
- Supports Random Forest and Gradient Boosting

### 4. Model Management (`app/ml/model_manager.py`)
- Model loading and serving
- Version management
- Canary deployment support
- A/B testing capabilities

### 5. API Layer (`app/api/`)
- FastAPI REST endpoints
- Real-time inference
- Batch inference
- Model management APIs
- Metrics endpoints

### 6. Database (`app/models.py`)
- PostgreSQL for persistence
- Prediction history
- Model metrics storage
- Model version registry

### 7. Services (`app/services/`)
- Business logic separation
- Prediction service
- Metrics service

### 8. Frontend (`frontend/`)
- React-based dashboard
- Real-time predictions
- Model monitoring
- Metrics visualization

## Data Flow

### Training Flow
1. Generate/load data → `scripts/generate_data.py`
2. Train model → `scripts/train_model.py`
3. Log to MLflow → Experiment tracking
4. Register model → Database + MLflow
5. Deploy → Model manager loads model

### Inference Flow
1. API request → FastAPI endpoint
2. Feature transformation → Feature store
3. Model prediction → Model manager
4. Store result → Database
5. Return response → Client

### Canary Flow
1. Train new model
2. Set as canary → `scripts/setup_canary.py`
3. Route % traffic → Prediction service
4. Monitor metrics → Dashboard
5. Promote if good → `scripts/setup_canary.py promote`

## Technology Stack

- **Backend**: FastAPI, Python 3.10+
- **ML**: scikit-learn, MLflow
- **Database**: PostgreSQL
- **Frontend**: React, Material-UI, Recharts
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus metrics

## Scalability

- Stateless API design (horizontal scaling)
- Database connection pooling
- Batch processing support
- Async request handling (FastAPI)

## Security Considerations

- Input validation (Pydantic schemas)
- SQL injection prevention (SQLAlchemy ORM)
- Environment variable configuration
- CORS configuration

## Future Enhancements

- Model retraining pipeline
- Automated canary promotion
- Real-time streaming inference
- Advanced monitoring (Grafana)
- Model explainability (SHAP)


