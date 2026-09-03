"""API catalog metadata for the developer portal."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.core.responses import success

router = APIRouter(prefix="/catalog", tags=["Catalog"])

CATALOG = [
    {
        "slug": "universities",
        "name": "Universities API",
        "description": "Search universities by name, country, and more.",
        "category": "Education",
        "version": "v1",
        "status": "stable",
        "authentication": "optional",
        "base_path": "/v1/universities",
        "rate_limit_anonymous": 60,
    },
    {
        "slug": "countries",
        "name": "Countries API",
        "description": "Country metadata, states, and sample cities.",
        "category": "Geography",
        "version": "v1",
        "status": "stable",
        "authentication": "optional",
        "base_path": "/v1/countries",
        "rate_limit_anonymous": 60,
    },
    {
        "slug": "geography",
        "name": "Geography API",
        "description": "Geocoding, reverse geocoding, and distance.",
        "category": "Geography",
        "version": "v1",
        "status": "stable",
        "authentication": "optional",
        "base_path": "/v1",
        "rate_limit_anonymous": 60,
    },
    {
        "slug": "weather",
        "name": "Weather API",
        "description": "Current weather, forecast, and historical.",
        "category": "Weather",
        "version": "v1",
        "status": "stable",
        "authentication": "optional",
        "base_path": "/v1/weather",
        "rate_limit_anonymous": 60,
    },
    {
        "slug": "books",
        "name": "Books API",
        "description": "Search books by title, author, or ISBN.",
        "category": "Books",
        "version": "v1",
        "status": "stable",
        "authentication": "optional",
        "base_path": "/v1/books",
        "rate_limit_anonymous": 60,
    },
    {
        "slug": "currency",
        "name": "Currency API",
        "description": "FX rates and currency conversion.",
        "category": "Finance",
        "version": "v1",
        "status": "stable",
        "authentication": "optional",
        "base_path": "/v1",
        "rate_limit_anonymous": 60,
    },
    {
        "slug": "time",
        "name": "Time API",
        "description": "Current time, conversion, and IANA timezones.",
        "category": "Utilities",
        "version": "v1",
        "status": "stable",
        "authentication": "optional",
        "base_path": "/v1",
        "rate_limit_anonymous": 60,
    },
]


@router.get("", summary="List available APIs")
async def list_catalog(request: Request):
    return success(CATALOG, request_id=getattr(request.state, "request_id", None))
