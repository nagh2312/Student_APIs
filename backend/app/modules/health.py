"""Health and metrics endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

router = APIRouter(tags=["Health"])

REQUEST_COUNT = Counter(
    "student_api_requests_total",
    "Total API requests",
    ["endpoint", "method", "status"],
)


@router.get("/health", summary="Liveness + basic status")
async def health(request: Request):
    return {
        "status": "ok",
        "service": "student-api-platform",
        "mock_mode": getattr(request.app.state, "mock_mode", True),
    }


@router.get("/health/live", summary="Kubernetes-style liveness")
async def live():
    return {"status": "alive"}


@router.get("/health/ready", summary="Readiness (deps)")
async def ready(request: Request):
    redis_ok = True
    redis = getattr(request.app.state, "redis", None)
    if redis is not None:
        try:
            await redis.ping()
        except Exception:
            redis_ok = False
    status = "ready" if redis_ok else "degraded"
    return {"status": status, "redis": redis_ok}


@router.get("/metrics", summary="Prometheus metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
