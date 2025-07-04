# NOFACE.digital Bot - Professional Makefile
# Development and deployment automation

.PHONY: help install dev prod clean test lint format docker logs

# Default target
.DEFAULT_GOAL := help

# Configuration
PYTHON := python3
PIP := pip3
VENV := venv
DOCKER_IMAGE := nofacebot
DOCKER_TAG := latest

# Colors for output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

help: ## Show this help message
	@echo "$(BLUE)NOFACE.digital Bot - Professional Edition$(RESET)"
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'

install: ## Install dependencies and setup environment
	@echo "$(YELLOW)Setting up development environment...$(RESET)"
	$(PYTHON) -m venv $(VENV)
	./$(VENV)/bin/pip install --upgrade pip setuptools wheel
	./$(VENV)/bin/pip install -r requirements.txt
	@echo "$(GREEN)✅ Environment setup complete!$(RESET)"
	@echo "$(BLUE)Activate with: source $(VENV)/bin/activate$(RESET)"

install-prod: ## Install production dependencies only
	@echo "$(YELLOW)Installing production dependencies...$(RESET)"
	$(PIP) install --no-dev -r requirements.txt
	@echo "$(GREEN)✅ Production dependencies installed!$(RESET)"

dev: ## Run bot in development mode
	@echo "$(YELLOW)Starting bot in development mode...$(RESET)"
	@export DEBUG=true && export LOG_LEVEL=DEBUG && $(PYTHON) main.py

prod: ## Run bot in production mode
	@echo "$(YELLOW)Starting bot in production mode...$(RESET)"
	@export DEBUG=false && export LOG_LEVEL=INFO && $(PYTHON) main.py

test: ## Run tests
	@echo "$(YELLOW)Running tests...$(RESET)"
	$(PYTHON) -m pytest tests/ -v --cov=app --cov-report=html
	@echo "$(GREEN)✅ Tests completed!$(RESET)"

lint: ## Run code linting
	@echo "$(YELLOW)Running code linting...$(RESET)"
	$(PYTHON) -m flake8 app/ --max-line-length=100 --ignore=E203,W503
	$(PYTHON) -m mypy app/ --ignore-missing-imports
	@echo "$(GREEN)✅ Linting completed!$(RESET)"

format: ## Format code with black
	@echo "$(YELLOW)Formatting code...$(RESET)"
	$(PYTHON) -m black app/ --line-length=100
	$(PYTHON) -m isort app/ --profile=black
	@echo "$(GREEN)✅ Code formatted!$(RESET)"

clean: ## Clean up generated files
	@echo "$(YELLOW)Cleaning up...$(RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/
	@echo "$(GREEN)✅ Cleanup completed!$(RESET)"

# Docker commands
docker-build: ## Build Docker image
	@echo "$(YELLOW)Building Docker image...$(RESET)"
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "$(GREEN)✅ Docker image built!$(RESET)"

docker-run: ## Run bot in Docker container
	@echo "$(YELLOW)Running bot in Docker...$(RESET)"
	docker run --rm --env-file .env -v $(PWD)/data:/app/data -v $(PWD)/logs:/app/logs $(DOCKER_IMAGE):$(DOCKER_TAG)

docker-dev: ## Run Docker compose for development
	@echo "$(YELLOW)Starting development environment with Docker Compose...$(RESET)"
	docker-compose -f docker-compose.yml up --build

docker-prod: ## Run Docker compose for production
	@echo "$(YELLOW)Starting production environment...$(RESET)"
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

docker-stop: ## Stop Docker compose
	@echo "$(YELLOW)Stopping Docker environment...$(RESET)"
	docker-compose down
	@echo "$(GREEN)✅ Docker environment stopped!$(RESET)"

docker-logs: ## View Docker logs
	@echo "$(YELLOW)Viewing Docker logs...$(RESET)"
	docker-compose logs -f noface-bot

# Database commands
db-migrate: ## Run database migrations
	@echo "$(YELLOW)Running database migrations...$(RESET)"
	alembic upgrade head
	@echo "$(GREEN)✅ Migrations completed!$(RESET)"

db-reset: ## Reset database (development only)
	@echo "$(RED)⚠️  Resetting database...$(RESET)"
	rm -f app.db
	$(PYTHON) -c "from app.models.base import create_tables; create_tables()"
	@echo "$(GREEN)✅ Database reset!$(RESET)"

# Monitoring
logs: ## View application logs
	@echo "$(YELLOW)Viewing logs...$(RESET)"
	tail -f logs/bot_$(shell date +%Y%m%d).log

monitor: ## Start monitoring dashboard
	@echo "$(YELLOW)Starting monitoring...$(RESET)"
	@echo "$(BLUE)Prometheus: http://localhost:9090$(RESET)"
	@echo "$(BLUE)Grafana: http://localhost:3000 (admin/admin)$(RESET)"
	docker-compose up prometheus grafana

# Security
security-check: ## Run security checks
	@echo "$(YELLOW)Running security checks...$(RESET)"
	$(PYTHON) -m safety check
	$(PYTHON) -m bandit -r app/
	@echo "$(GREEN)✅ Security checks completed!$(RESET)"

# Deployment
deploy-staging: ## Deploy to staging
	@echo "$(YELLOW)Deploying to staging...$(RESET)"
	# Add your staging deployment commands here
	@echo "$(GREEN)✅ Deployed to staging!$(RESET)"

deploy-prod: ## Deploy to production
	@echo "$(RED)⚠️  Deploying to production...$(RESET)"
	# Add your production deployment commands here
	@echo "$(GREEN)✅ Deployed to production!$(RESET)"

# Setup commands
setup-env: ## Setup environment file
	@echo "$(YELLOW)Setting up environment...$(RESET)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✅ Created .env file from template$(RESET)"; \
		echo "$(YELLOW)📝 Please edit .env file with your settings$(RESET)"; \
	else \
		echo "$(BLUE)ℹ️  .env file already exists$(RESET)"; \
	fi

setup-hooks: ## Setup git hooks
	@echo "$(YELLOW)Setting up git hooks...$(RESET)"
	cp scripts/pre-commit .git/hooks/
	chmod +x .git/hooks/pre-commit
	@echo "$(GREEN)✅ Git hooks installed!$(RESET)"

# All-in-one commands
setup: install setup-env setup-hooks ## Complete project setup
	@echo "$(GREEN)🎉 Project setup completed!$(RESET)"
	@echo "$(BLUE)Next steps:$(RESET)"
	@echo "  1. Edit .env file with your settings"
	@echo "  2. Run 'make dev' to start development"

quick-start: setup dev ## Quick start for new developers 