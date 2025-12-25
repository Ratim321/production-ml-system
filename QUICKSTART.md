# Quick Start Guide

Get the ML Churn Prediction System up and running in 5 minutes!

## Step 1: Start Services

```bash
# Start all services with Docker Compose
docker-compose up -d

# Wait for services to be ready (about 30 seconds)
docker-compose ps
```

## Step 2: Initialize Database

```bash
# Initialize database tables
docker exec -it ml_api python scripts/init_db.py
```

## Step 3: Generate Training Data

```bash
# Generate synthetic customer data
docker exec -it ml_api python scripts/generate_data.py
```

## Step 4: Train Model

```bash
# Train the initial model
docker exec -it ml_api python scripts/train_model.py
```

You should see output like:
```
Loaded 5000 samples
Churn rate: 26.54%
Training model...
Model trained! MLflow run ID: abc123def456
```

## Step 5: Test the API

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Make a prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {
      "customer_id": "CUST_00001",
      "age": 45,
      "tenure": 12,
      "monthly_charges": 70.5,
      "total_charges": 846.0,
      "contract_type": "Month-to-month",
      "payment_method": "Electronic check",
      "paperless_billing": true,
      "gender": "Male",
      "partner": false,
      "dependents": false,
      "phone_service": true,
      "multiple_lines": false,
      "internet_service": "Fiber optic",
      "online_security": false,
      "online_backup": false,
      "device_protection": false,
      "tech_support": false,
      "streaming_tv": true,
      "streaming_movies": true
    }
  }'
```

## Step 6: Access the Dashboard

Open your browser and navigate to:
- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5000

## Next Steps

- View model metrics in the dashboard
- Try batch inference: `docker exec -it ml_api python scripts/batch_inference.py`
- Set up canary deployment (see DEPLOYMENT.md)
- Explore the API endpoints at http://localhost:8000/docs

## Troubleshooting

### Services not starting?
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart
```

### Database connection errors?
```bash
# Wait a bit longer for PostgreSQL to be ready
docker-compose ps postgres
# Should show "healthy" status
```

### Model not loading?
- Make sure you've trained a model (Step 4)
- Check MLflow is accessible: http://localhost:5000
- Verify model files exist: `docker exec -it ml_api ls -la models/`

## Using Make Commands

For convenience, you can use the Makefile:

```bash
make all          # Complete setup
make train        # Train model
make test         # Run tests
make canary-setup VERSION=v20240101_120000 TRAFFIC=10
```

Happy predicting! 🚀


