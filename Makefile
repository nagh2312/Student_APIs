.PHONY: dev test lint format migrate seed ingest build up down

dev:
	docker compose up --build

up:
	docker compose up -d --build

down:
	docker compose down

test:
	cd backend && MOCK_MODE=true pytest -q
	cd frontend && npm test --if-present

lint:
	cd backend && ruff check app tests
	cd frontend && npm run lint

format:
	cd backend && ruff format app tests
	cd frontend && npx prettier --write "src/**/*.{ts,tsx}" || true

migrate:
	@echo "Migrations: use alembic when MOCK_MODE=false (see backend/README.md)"

seed:
	cd backend && python -m scripts.seed.seed_all

ingest:
	cd backend && python -m scripts.ingest.universities

build:
	docker compose build
