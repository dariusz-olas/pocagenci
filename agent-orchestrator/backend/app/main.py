"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.dependencies import init_dependencies, cleanup_dependencies
from app.api.routes import tasks, costs, health
from app.api.websockets import progress


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    settings = get_settings()
    print(f"Starting {settings.app_name}...")

    # Initialize dependencies
    await init_dependencies(settings)

    yield

    # Cleanup
    await cleanup_dependencies()
    print("Shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Meta-framework for AI agent orchestration",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(health.router)
    app.include_router(tasks.router, prefix="/api/v1")
    app.include_router(costs.router, prefix="/api/v1")
    app.include_router(progress.router)

    return app


# Create app instance
app = create_app()
