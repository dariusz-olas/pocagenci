# Agent Orchestrator - Setup Guide

## Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)

## Configuration

### 1. Environment Variables

Copy the example environment file and configure:

```bash
cd backend
cp .env.example .env
```

**Required variables:**

- `API_KEY`: Generate a secure key (min 32 characters):
  ```bash
  openssl rand -hex 32
  ```
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string

**Optional variables:**

- `CORS_ORIGINS`: JSON array of allowed origins (default: localhost)
- `DAILY_BUDGET_USD`: Daily LLM budget limit (default: 5.0)
- `EXECUTION_LLM_URL`: Local LLM URL (default: Ollama)

### 2. Production Deployment

Use `docker-compose.prod.yml` for production:

```bash
# Set environment variables
export API_KEY=$(openssl rand -hex 32)
export ANTHROPIC_API_KEY=your-key-here
export CORS_ORIGINS='["https://yourdomain.com"]'
export POSTGRES_PASSWORD=$(openssl rand -hex 16)

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f api
```

### 3. Development Setup

Use `docker-compose.yml` for development:

```bash
# Set required environment variables
export API_KEY=$(openssl rand -hex 32)
export ANTHROPIC_API_KEY=your-key-here

# Start services
docker-compose up -d

# Watch logs
docker-compose logs -f api
```

## Database Migrations

### From Docker Container
```bash
docker-compose exec api alembic upgrade head
```

### From Host (Linux/Mac)
```bash
cd backend
source .venv/bin/activate  # lub .venv\Scripts\activate na Windows
alembic upgrade head
```

### From Host (Windows)
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
alembic upgrade head
```

**Uwaga:** Migracje z hosta wymagają `psycopg2-binary` i używają `localhost` zamiast `db` jako hosta (automatycznie konwertowane w `alembic/env.py`).

Więcej informacji: [MIGRATION_SETUP.md](backend/MIGRATION_SETUP.md)

## Health Checks

- API: http://localhost:8000/health
- Frontend: http://localhost:3000

## Security Notes

⚠️ **IMPORTANT:**

1. **Never use default API keys in production**
2. **API_KEY must be at least 32 characters**
3. **Configure CORS_ORIGINS for your domain**
4. **Use strong PostgreSQL password**
5. **Keep secrets in environment variables, not in code**

## Rate Limits

- General endpoints: 100 requests/minute per API key
- `/tasks/decompose`: 10 requests/minute per API key

## Monitoring

Application uses structured logging (JSON in production):

```bash
# View logs
docker-compose logs -f api

# Filter by level
docker-compose logs api | grep '"level":"error"'
```

## Troubleshooting

### API key validation error

Ensure your API_KEY is at least 32 characters:
```bash
echo -n "your-key" | wc -c
```

### CORS errors

Add your frontend domain to CORS_ORIGINS:
```bash
export CORS_ORIGINS='["https://yourdomain.com","http://localhost:3000"]'
```

### Database connection failed

Check DATABASE_URL format:
```
postgresql+asyncpg://user:password@host:port/database
```

## Windows ARM64 Support

Projekt jest w pełni wspierany na Windows ARM64:

- **Quick Start:** [QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md)
- **Detailed Guide:** [SETUP_WINDOWS_ARM64.md](SETUP_WINDOWS_ARM64.md)
- **PowerShell Scripts:** `setup-windows.ps1` (alternatywa dla Makefile)
- **Troubleshooting:** [TROUBLESHOOTING_DOCKER.md](TROUBLESHOOTING_DOCKER.md)
- **Changelog:** [CHANGELOG_WINDOWS_SETUP.md](CHANGELOG_WINDOWS_SETUP.md)

## Resources

- Documentation: See PRODUCTION_READINESS.md
- Issues: Check TASKS.md for known issues
- Windows Setup: See SETUP_WINDOWS_ARM64.md
