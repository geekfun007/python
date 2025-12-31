# ============================================
# FastAPI Demo Makefile
# ============================================

.PHONY: help install dev test lint format docker-build docker-up docker-down clean

# Default target
help:
	@echo "FastAPI Demo - Available commands:"
	@echo ""
	@echo "  make install      - Install dependencies"
	@echo "  make dev          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linter"
	@echo "  make format       - Format code"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start Docker services"
	@echo "  make docker-down  - Stop Docker services"
	@echo "  make clean        - Clean up"
	@echo ""

# Install dependencies
install:
	pip install --upgrade pip
	pip install -r requirements.txt

# Run development server
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run production server
prod:
	gunicorn app.main:app \
		--worker-class uvicorn.workers.UvicornWorker \
		--bind 0.0.0.0:8000 \
		--workers 4

# Run tests
test:
	pytest -v

# Run tests with coverage
test-cov:
	pytest --cov=app --cov-report=html --cov-report=term-missing

# Run linter
lint:
	flake8 app tests
	mypy app

# Format code
format:
	black app tests
	isort app tests

# Build Docker image
docker-build:
	docker-compose build

# Start Docker services
docker-up:
	docker-compose up -d

# Stop Docker services
docker-down:
	docker-compose down

# Start production Docker services
docker-prod-up:
	docker-compose -f docker-compose.prod.yml up -d

# Stop production Docker services
docker-prod-down:
	docker-compose -f docker-compose.prod.yml down

# View logs
docker-logs:
	docker-compose logs -f

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".mypy_cache" -delete
	find . -type d -name "htmlcov" -delete
	find . -type f -name ".coverage" -delete

# Initialize database
init-db:
	docker-compose exec mysql mysql -uroot -prootpassword fastapi_demo < sql/001_create_database.sql
	docker-compose exec mysql mysql -uroot -prootpassword fastapi_demo < sql/002_seed_data.sql

# Generate Thrift code (if using thrift compiler)
thrift-gen:
	thrift -r --gen py -out . thrift/user.thrift
	thrift -r --gen py -out . thrift/article.thrift
	thrift -r --gen py -out . thrift/common.thrift
