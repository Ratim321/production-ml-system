# 🚀 Production ML System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![MLflow](https://img.shields.io/badge/MLflow-2.8-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**A complete, production-ready machine learning system for customer churn prediction with real-time and batch inference capabilities.**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 What is This Project?

### The Problem
**Customer churn** is when customers stop using a company's service. For businesses, losing customers is expensive - it costs more to acquire new customers than to retain existing ones. Companies need to identify customers who are likely to churn **before** they leave, so they can take action to retain them.

### The Solution
This project is a **complete machine learning system** that predicts which customers are likely to churn. It's not just a Jupyter notebook - it's a **production-ready application** that can be deployed and used by real businesses.

### What Makes It "Production-Ready"?
Unlike simple ML demos, this system includes everything needed for real-world deployment:

- **REST API** - Other applications can call it to get predictions
- **Web Dashboard** - Business users can interact with it visually
- **Model Versioning** - Track which models perform best
- **Canary Deployments** - Safely roll out new models
- **Batch Processing** - Handle thousands of predictions at once
- **Monitoring** - Track performance and system health
- **Testing** - Comprehensive test coverage
- **Docker** - Easy deployment anywhere

### Real-World Use Case
Imagine a telecom company wants to reduce customer churn. They can:
1. Send customer data to this system via API
2. Get predictions about which customers might leave
3. Take proactive actions (offers, discounts, support) to retain at-risk customers
4. Monitor model performance and improve over time

### Example Scenario

**Customer Profile:**
- Age: 45
- Tenure: 12 months (relatively new)
- Monthly Charges: $70 (above average)
- Contract: Month-to-month (flexible)
- Payment: Electronic check
- No online security or tech support

**Prediction:** 75% churn probability ⚠️

**Business Action:** 
- Offer a 6-month contract with 20% discount
- Add free tech support
- Proactive customer service call

**Result:** Customer retention improves, revenue protected

### Who Is This For?
- **ML Engineers** - Learn production ML system design
- **Data Scientists** - See how to move from notebooks to production
- **Software Engineers** - Understand ML system architecture
- **Students** - Portfolio project demonstrating full-stack ML skills
- **Companies** - Template for building their own ML systems

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 How It Works

### The ML Pipeline

1. **Data Generation** → Creates synthetic customer data (age, tenure, charges, services, etc.)
2. **Feature Engineering** → Transforms raw data into features the model can understand
3. **Model Training** → Trains a machine learning model (Random Forest) to predict churn probability
4. **Model Deployment** → Serves the model via REST API for real-time predictions
5. **Monitoring** → Tracks predictions and model performance over time

### What the Model Predicts

The system analyzes customer characteristics and predicts:
- **Churn Probability** (0-100%): How likely the customer is to leave
- **Binary Prediction** (Yes/No): Will the customer churn?
- **Risk Factors**: Which features contribute most to churn risk

### Model Features Analyzed

The model considers 19 different customer attributes:
- Demographics (age, gender, partner, dependents)
- Service details (phone, internet, streaming services)
- Contract information (type, payment method, billing)
- Financial metrics (monthly charges, total charges, tenure)

### Example Prediction Flow

```
Customer Data → API Request → Feature Transformation → ML Model → Churn Probability
                                                                    ↓
                                                          Business Action (retention offer)
```

**Input**: Customer information (age: 45, tenure: 12 months, monthly charges: $70, etc.)  
**Output**: Churn probability (e.g., 0.75 = 75% chance of churning)  
**Action**: Company can offer a discount or special service to retain the customer

### Key Components

- ✅ **Complete ML pipeline** (data → features → training → inference)
- ✅ **RESTful API** with real-time and batch inference
- ✅ **Model versioning** and experiment tracking (MLflow)
- ✅ **Feature store** for consistent transformations
- ✅ **Canary deployment** support for safe model rollouts
- ✅ **React dashboard** for monitoring and visualization
- ✅ **Comprehensive test suite** for reliability
- ✅ **CI/CD pipeline** for automated testing and deployment
- ✅ **Docker containerization** for easy deployment

## ✨ Features

### Core ML Pipeline
- **Data Pipeline**: Synthetic data generation and preprocessing
- **Feature Store**: Consistent feature engineering across training and inference
- **Model Training**: scikit-learn with MLflow experiment tracking
- **Model Registry**: Version management and performance tracking

### API Endpoints
- `POST /api/v1/predict` - Real-time single prediction
- `POST /api/v1/predict/batch` - Batch inference
- `GET /api/v1/models` - List all model versions
- `GET /api/v1/models/{version}` - Get model details
- `GET /api/v1/metrics` - Model performance metrics
- `GET /api/v1/health` - System health check

### Advanced MLOps Features
- **Canary Deployments**: Gradual rollout with traffic splitting
- **A/B Testing**: Compare model versions side-by-side
- **Batch Processing**: Efficient bulk inference
- **Real-time Inference**: Low-latency predictions
- **Metrics Dashboard**: Visualize model performance
- **Prometheus Metrics**: Standard monitoring endpoints

### Quality Assurance
- Unit and integration tests
- Code coverage reporting
- Linting and formatting
- Type safety with Pydantic

## 🏗️ Architecture

```
┌─────────────────┐
│   React Frontend │  ← User Interface
└────────┬─────────┘
         │
┌────────▼─────────┐
│   FastAPI Backend │  ← REST API
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│Postgres│ │ MLflow │  ← Data & Models
└────────┘ └────────┘
```

### Technology Stack

- **Backend**: FastAPI, Python 3.10+
- **ML Framework**: scikit-learn, MLflow
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: React, Material-UI, Recharts
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus metrics

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for local development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/production-ml-system.git
cd production-ml-system
```

> **Note**: Replace `yourusername` with your GitHub username in all URLs

# Start all services
docker-compose up -d

# Initialize database
docker exec -it ml_api python scripts/init_db.py

# Generate training data
docker exec -it ml_api python scripts/generate_data.py

# Train initial model
docker exec -it ml_api python scripts/train_model.py
```

**Access the services:**
- 🌐 **Frontend Dashboard**: http://localhost:3000
- 📚 **API Documentation**: http://localhost:8000/docs
- 📊 **MLflow UI**: http://localhost:5000
- 🔍 **API Health**: http://localhost:8000/api/v1/health

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
alembic upgrade head

# Generate data and train model
python scripts/generate_data.py
python scripts/train_model.py

# Start API server
uvicorn app.main:app --reload --port 8000

# In another terminal, start frontend
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
production-ml-system/
├── app/                      # FastAPI application
│   ├── api/v1/              # API routes
│   ├── ml/                  # ML components
│   │   ├── model_manager.py # Model loading & serving
│   │   └── trainer.py       # Model training
│   ├── services/            # Business logic
│   ├── feature_store/       # Feature engineering
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   └── main.py              # FastAPI app
├── scripts/                  # Utility scripts
│   ├── train_model.py       # Training pipeline
│   ├── batch_inference.py   # Batch processing
│   ├── generate_data.py     # Data generation
│   └── setup_canary.py      # Canary deployment
├── tests/                   # Test suite
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── frontend/                # React dashboard
│   ├── src/
│   └── public/
├── docker/                   # Docker configuration
├── .github/workflows/        # CI/CD pipeline
├── alembic/                 # Database migrations
├── docker-compose.yml       # Docker Compose config
└── requirements.txt         # Python dependencies
```

## 📚 API Documentation

### Real-time Prediction

```bash
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

### Batch Inference

```bash
curl -X POST http://localhost:8000/api/v1/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "customers": [...]
  }'
```

Full API documentation available at http://localhost:8000/docs

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test suites
pytest tests/unit/
pytest tests/integration/
```

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions, including:
- Production configuration
- Canary deployment setup
- Scaling strategies
- Monitoring setup

## 📖 Documentation

- [QUICKSTART.md](QUICKSTART.md) - 5-minute quick start guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture details
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment and operations guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [PROJECT_SHOWCASE.md](PROJECT_SHOWCASE.md) - Project showcase details

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Project Stats

- **Lines of Code**: 3000+
- **Components**: 20+ modules
- **API Endpoints**: 8+ REST endpoints
- **Test Coverage**: Unit + Integration tests
- **Services**: 4 containerized services

## 🎓 Use Cases & Applications

### For Learning
- **Understand MLOps**: See how ML models move from development to production
- **Learn Best Practices**: Production-ready patterns and architecture
- **Portfolio Project**: Showcase full-stack ML engineering skills
- **Interview Prep**: Demonstrate end-to-end ML system knowledge

### For Business
- **Customer Retention**: Identify at-risk customers before they churn
- **Resource Allocation**: Focus retention efforts on high-risk customers
- **Cost Reduction**: Reduce customer acquisition costs by improving retention
- **Data-Driven Decisions**: Make retention strategies based on ML predictions

### For Development
- **Template**: Starting point for your own ML projects
- **Reference Implementation**: See how to structure production ML systems
- **Integration Example**: Learn how to integrate ML into existing applications
- **Deployment Guide**: Follow deployment patterns for your own models

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built as a showcase of production-ready ML system architecture and MLOps best practices.

---

<div align="center">

**⭐ If you find this project helpful, please give it a star! ⭐**

Made with ❤️ for the ML community

</div>
