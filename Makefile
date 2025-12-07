.PHONY: help backend frontend install-backend install-frontend

help:
	@echo "ClashAI - Available commands:"
	@echo "  make backend          - Start backend server"
	@echo "  make frontend         - Start frontend server"
	@echo "  make install-backend  - Install backend dependencies"
	@echo "  make install-frontend - Install frontend dependencies"

backend:
	@echo "Starting backend server..."
	cd backend && uvicorn main:app --reload --port 8000

frontend:
	@echo "Starting frontend server..."
	cd frontend && bun run dev

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && bun install
