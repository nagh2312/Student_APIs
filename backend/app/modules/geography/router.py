"""Geography API router."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.core.config import get_settings
from app.core.dependencies import optional_api_key
from app.core.exceptions import ValidationAppError
from app.core.responses import success
from app.modules.geography.providers.base import (
    compute_distance,
    get_geography_provider,
)

router = APIRouter(tags=["Geography"])


def _provider():
    s = get_settings()
    return get_geography_provider(mock_mode=s.mock_mode, provider_name=s.geography_provider)


@router.get("/geocode", summary="Forward geocode a place name")
async def geocode(
    request: Request,
    q: str = Query(..., min_length=1, description="Place name or address"),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    results = await _provider().geocode(q)
    return success(
        [r.model_dump() for r in results],
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/reverse-geocode", summary="Reverse geocode coordinates")
async def reverse_geocode(
    request: Request,
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    result = await _provider().reverse_geocode(lat, lon)
    return success(
        result.model_dump(),
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/distance", summary="Great-circle distance between two points")
async def distance(
    request: Request,
    from_lat: float = Query(...),
    from_lon: float = Query(...),
    to_lat: float = Query(...),
    to_lon: float = Query(...),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    result = compute_distance(from_lat, from_lon, to_lat, to_lon)
    return success(
        result.model_dump(),
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/coordinates/{place}", summary="Resolve coordinates for a known place")
async def coordinates(
    place: str,
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    if not place.strip():
        raise ValidationAppError("Place name is required")
    results = await _provider().geocode(place)
    return success(
        results[0].model_dump(),
        request_id=getattr(request.state, "request_id", None),
    )
