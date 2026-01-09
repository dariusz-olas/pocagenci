.PHONY: install dev test lint clean docker-up docker-down migrate

# === Installation ===
install:
	cd backend && pip install -e ".[dev]"
	cd frontend && npm install

# === Development ===
dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# === Testing ===
test:
	cd backend && pytest -v --cov=app

test-watch:
	cd backend && pytest -v --watch

# === Linting ===
lint:
	cd backend && ruff check app tests
	cd frontend && npm run lint

format:
	cd backend && ruff format app tests

# === Database ===
migrate:
	cd backend && alembic upgrade head

migrate-create:
	cd backend && alembic revision --autogenerate -m "$(name)"

# === Docker ===
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# === Cleanup ===
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name node_modules -exec rm -rf {} +
