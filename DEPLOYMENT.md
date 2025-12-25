# Deployment Guide

## Quick Start with Docker

1. **Clone and navigate to the project:**
   ```bash
   git clone <your-repo-url>
   cd project
   ```

2. **Start all services:**
   ```bash
   docker-compose up -d
   ```

3. **Initialize database:**
   ```bash
   docker exec -it ml_api python scripts/init_db.py
   ```

4. **Generate training data:**
   ```bash
   docker exec -it ml_api python scripts/generate_data.py
   ```

5. **Train initial model:**
   ```bash
   docker exec -it ml_api python scripts/train_model.py
   ```

6. **Access services:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Frontend: http://localhost:3000
   - MLflow UI: http://localhost:5000

## Canary Deployment

### Set up Canary Model

1. Train a new model:
   ```bash
   docker exec -it ml_api python scripts/train_model.py
   ```

2. Note the model version from the output or MLflow UI

3. Set up canary deployment (10% traffic):
   ```bash
   docker exec -it ml_api python scripts/setup_canary.py setup --version v20240101_120000 --traffic 10
   ```

4. Monitor canary performance in the metrics dashboard

5. Promote canary to active when satisfied:
   ```bash
   docker exec -it ml_api python scripts/setup_canary.py promote --version v20240101_120000
   ```

## Batch Inference

Run batch inference on a dataset:

```bash
docker exec -it ml_api python scripts/batch_inference.py
```

Results will be saved to `data/predictions/batch_predictions.csv`

## Production Deployment

### Environment Variables

Create a `.env` file with production settings:

```env
DATABASE_URL=postgresql://user:password@prod-db:5432/mldb
MLFLOW_TRACKING_URI=http://mlflow-server:5000
API_HOST=0.0.0.0
API_PORT=8000
CANARY_TRAFFIC_PERCENT=10
```

### Scaling

To scale the API service:

```bash
docker-compose up -d --scale api=3
```

### Monitoring

- Prometheus metrics available at `/metrics`
- Health checks at `/api/v1/health`
- MLflow UI for experiment tracking

## CI/CD

The GitHub Actions workflow automatically:
- Runs tests on push/PR
- Lints code
- Builds Docker images

To deploy on merge to main, add deployment steps to `.github/workflows/ci.yml`


