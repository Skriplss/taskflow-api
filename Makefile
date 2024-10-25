.PHONY: help install install-dev run run-dev test test-cov lint format clean docker-build docker-up docker-down migrate

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

run: ## Run the application locally
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-dev: ## Run the application with Docker Compose (dev)
	docker-compose -f docker-compose.dev.yml up --build

run-prod: ## Run the application with Docker Compose (production)
	docker-compose up --build -d

test: ## Run tests
	pytest -v

test-cov: ## Run tests with coverage report
	pytest --cov=app --cov-report=html --cov-report=term -v

test-watch: ## Run tests in watch mode
	pytest-watch

lint: ## Run linters
	black --check app tests
	isort --check-only app tests
	flake8 app tests --max-line-length=100 --extend-ignore=E203,W503
	mypy app --ignore-missing-imports --no-strict-optional

format: ## Format code with black and isort
	black app tests
	isort app tests

clean: ## Clean up cache and build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/

docker-build: ## Build Docker image
	docker build -t task-api:latest .

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

migrate: ## Run database migrations
	alembic upgrade head

migrate-create: ## Create a new migration
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

migrate-rollback: ## Rollback last migration
	alembic downgrade -1

db-shell: ## Connect to database shell
	docker-compose exec db psql -U postgres -d taskdb

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

setup: install-dev ## Complete setup for development
	cp .env.example .env
	@echo "✅ Setup complete! Edit .env file with your settings."
	@echo "Run 'make run-dev' to start the application."

