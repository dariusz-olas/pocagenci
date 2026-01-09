"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.dependencies import init_dependencies, cleanup_dependencies
from app.api.routes import tasks, costs, health, executions
from app.api.websockets import progress
from app.logging_config import configure_logging, get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    settings = get_settings()

    # Configure logging first
    configure_logging(debug=settings.debug)

    logger.info("application_starting", app_name=settings.app_name, debug=settings.debug)

    # Initialize dependencies
    await init_dependencies(settings)

    logger.info("application_ready")

    yield

    # Cleanup
    logger.info("application_shutting_down")
    await cleanup_dependencies()
    logger.info("application_stopped")


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
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(health.router)
    app.include_router(tasks.router, prefix="/api/v1")
    app.include_router(costs.router, prefix="/api/v1")
    app.include_router(executions.router, prefix="/api/v1")
    app.include_router(progress.router)

    return app


# Create app instance
app = create_app()
