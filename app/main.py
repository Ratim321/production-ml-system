"""FastAPI application main file"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import predictions, models, metrics, health
from app.database import Base, engine
from app.config import settings
from prometheus_client import make_asgi_app, Counter, Histogram
import time

# Create database tables
Base.metadata.create_all(bind=engine)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

app = FastAPI(
    title="Production ML System API",
    description="Production-ready ML system for customer churn prediction with real-time and batch inference",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predictions.router, prefix="/api/v1")
app.include_router(models.router, prefix="/api/v1")
app.include_router(metrics.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    """Middleware for collecting metrics"""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(duration)
    
    return response


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Production ML System API",
        "version": "1.0.0",
        "docs": "/docs",
        "repository": "https://github.com/yourusername/production-ml-system"
    }


@app.get("/api/v1")
async def api_info():
    """API information"""
    return {
        "version": "v1",
        "endpoints": {
            "predict": "/api/v1/predict",
            "batch_predict": "/api/v1/predict/batch",
            "models": "/api/v1/models",
            "metrics": "/api/v1/metrics",
            "health": "/api/v1/health"
        }
    }


