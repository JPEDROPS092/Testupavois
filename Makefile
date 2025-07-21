# Makefile for TTS Application

.PHONY: help build run stop clean logs dev-backend dev-frontend

# Default target
help:
	@echo "Available commands:"
	@echo "  build        - Build the Docker image"
	@echo "  run          - Run the application with Docker Compose"
	@echo "  stop         - Stop the running containers"
	@echo "  clean        - Remove containers and images"
	@echo "  logs         - Show application logs"
	@echo "  dev-backend  - Run backend in development mode"
	@echo "  dev-frontend - Run frontend in development mode"

# Build the Docker image
build:
	docker-compose build

# Run the application
run:
	docker-compose up -d

# Run in foreground
run-fg:
	docker-compose up

# Stop the application
stop:
	docker-compose down

# Clean up Docker resources
clean:
	docker-compose down -v --rmi all
	docker system prune -f

# Show logs
logs:
	docker-compose logs -f tts-app

# Development mode - backend only
dev-backend:
	@echo "Make sure you have a Python virtual environment activated"
	@echo "Running backend in development mode..."
	cd backend && python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Development mode - frontend only
dev-frontend:
	@echo "Running frontend in development mode..."
	cd frontend && npm run dev

# Install dependencies for local development
dev-setup:
	@echo "Setting up development environment..."
	python3 -m venv venv
	@echo "Activate virtual environment with: source venv/bin/activate"
	@echo "Then run: pip install -r backend/requirements.txt"
	@echo "And: cd frontend && npm install"
