"""FastAPI application entrypoint."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.logging import setup_logging
from app.core.responses import failure
from app.database.base import Base
from app.database.connection import dispose_engine, get_engine
from app.middleware import RateLimitMiddleware, RequestContextMiddleware
from app.modules.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(settings.debug)
    app.state.mock_mode = settings.mock_mode
    app.state.redis = None

    # Redis (optional)
    try:
        redis = Redis.from_url(settings.redis_url, decode_responses=True)
        await redis.ping()
        app.state.redis = redis
    except Exception:
        app.state.redis = None

    # DB schema (skip in mock mode — APIs use in-memory data)
    if not settings.mock_mode:
        try:
            engine = get_engine()
            async with engine.begin() as conn:
                # Import models so metadata is populated
                from app.modules.auth import models as _auth_models  # noqa: F401
                from app.modules.countries import models as _country_models  # noqa: F401
                from app.modules.universities import models as _uni_models  # noqa: F401

                await conn.run_sync(Base.metadata.create_all)
        except Exception:
            # Allow boot without DB; endpoints that need DB will fail clearly
            pass

    yield

    if app.state.redis is not None:
        await app.state.redis.close()
    await dispose_engine()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Open-source standardized APIs for student developers. "
            "Anonymous access supported; optional API keys for higher rate limits. "
            f"Mock mode: {'enabled' if settings.mock_mode else 'disabled'}."
        ),
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        contact={"name": "Student API Platform", "url": "https://github.com"},
        license_info={"name": "Apache-2.0"},
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[
            "X-Request-ID",
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Reset",
            "X-Response-Time-Ms",
        ],
    )
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(RequestContextMiddleware)

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        request_id = getattr(request.state, "request_id", None)
        return JSONResponse(
            status_code=exc.status_code,
            content=failure(
                code=exc.code,
                message=exc.message,
                request_id=request_id,
                details=exc.details,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        request_id = getattr(request.state, "request_id", None)
        return JSONResponse(
            status_code=400,
            content=failure(
                code="VALIDATION_ERROR",
                message="Invalid request parameters",
                request_id=request_id,
                details=exc.errors(),
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_handler(request: Request, exc: StarletteHTTPException):
        request_id = getattr(request.state, "request_id", None)
        code = "RESOURCE_NOT_FOUND" if exc.status_code == 404 else "HTTP_ERROR"
        detail = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return JSONResponse(
            status_code=exc.status_code,
            content=failure(code=code, message=detail, request_id=request_id),
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", None)
        return JSONResponse(
            status_code=500,
            content=failure(
                code="INTERNAL_ERROR",
                message="An unexpected error occurred",
                request_id=request_id,
            ),
        )

    app.include_router(health_router)
    app.include_router(api_v1_router, prefix="/v1")

    return app


app = create_app()
