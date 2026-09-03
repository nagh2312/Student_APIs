"""HTTP middleware: request ID, secure headers, rate limiting."""

from __future__ import annotations

import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import get_settings
from app.core.rate_limit import check_rate_limit, resolve_limit
from app.core.responses import failure


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex[:16]}"
        request.state.request_id = request_id
        request.state.authenticated = False
        started = time.perf_counter()

        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - started) * 1000

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time-Ms"] = f"{elapsed_ms:.2f}"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    SKIP_PREFIXES = ("/health", "/metrics", "/docs", "/redoc", "/openapi.json")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path
        if any(path.startswith(p) for p in self.SKIP_PREFIXES):
            return await call_next(request)

        settings = get_settings()
        api_key = request.headers.get("X-API-Key")
        authenticated = bool(api_key)
        request.state.authenticated = authenticated
        request.state.api_key = api_key

        client_host = request.client.host if request.client else "unknown"
        identity = f"key:{api_key[:16]}" if api_key else f"ip:{client_host}"
        limit = resolve_limit(settings, authenticated)
        redis = getattr(request.app.state, "redis", None)

        result = await check_rate_limit(
            redis,
            key=identity,
            limit=limit,
            window_seconds=settings.rate_limit_window_seconds,
        )

        if not result.allowed:
            request_id = getattr(request.state, "request_id", None)
            body = failure(
                code="RATE_LIMIT_EXCEEDED",
                message="Rate limit exceeded. Provide an API key for higher limits.",
                request_id=request_id,
            )
            response = JSONResponse(status_code=429, content=body)
            response.headers["X-RateLimit-Limit"] = str(result.limit)
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers["X-RateLimit-Reset"] = str(result.reset_at)
            response.headers["Retry-After"] = str(
                max(1, result.reset_at - int(time.time()))
            )
            return response

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(result.limit)
        response.headers["X-RateLimit-Remaining"] = str(result.remaining)
        response.headers["X-RateLimit-Reset"] = str(result.reset_at)
        return response
