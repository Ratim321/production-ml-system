.PHONY: help setup up down build test train init-db generate-data batch-inference clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Initial setup - create directories and copy env file
	@mkdir -p data/raw data/predictions models mlruns feature_store
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file. Please edit it with your configuration."; fi

up: ## Start all services with docker-compose
	docker-compose up -d

down: ## Stop all services
	docker-compose down

build: ## Build Docker images
	docker-compose build

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ --cov=app --cov-report=html

init-db: ## Initialize database
	python scripts/init_db.py

generate-data: ## Generate synthetic training data
	python scripts/generate_data.py

train: ## Train ML model
	python scripts/train_model.py

batch-inference: ## Run batch inference
	python scripts/batch_inference.py

canary-setup: ## Set up canary deployment (usage: make canary-setup VERSION=v20240101_120000 TRAFFIC=10)
	python scripts/setup_canary.py setup --version $(VERSION) --traffic $(TRAFFIC)

canary-promote: ## Promote canary to active (usage: make canary-promote VERSION=v20240101_120000)
	python scripts/setup_canary.py promote --version $(VERSION)

clean: ## Clean generated files
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

docker-clean: ## Clean Docker containers and volumes
	docker-compose down -v
	docker system prune -f

all: setup up ## Complete setup and start services
	@echo "Waiting for services to be ready..."
	@sleep 10
	@echo "Services started! Access:"
	@echo "  - API: http://localhost:8000"
	@echo "  - Frontend: http://localhost:3000"
	@echo "  - MLflow: http://localhost:5000"


