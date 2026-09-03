"""Countries service and router."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.core.dependencies import optional_api_key
from app.core.exceptions import NotFoundError, ValidationAppError
from app.core.responses import clamp_pagination, success
from app.modules.countries.schemas import MOCK_COUNTRIES, CountryOut, PlaceOut

router = APIRouter(prefix="/countries", tags=["Countries"])


def _public(c: dict) -> dict:
    return {k: v for k, v in c.items() if k not in {"states", "cities"}}


def _find(code: str) -> dict | None:
    code = code.upper()
    for c in MOCK_COUNTRIES:
        if c["code"] == code or c["code3"] == code:
            return c
    return None


@router.get("", summary="List countries")
async def list_countries(
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    region: str | None = None,
    q: str | None = None,
):
    page, limit = clamp_pagination(page, limit)
    items = list(MOCK_COUNTRIES)
    if region:
        items = [c for c in items if (c.get("region") or "").lower() == region.lower()]
    if q:
        needle = q.lower()
        items = [
            c
            for c in items
            if needle in c["name"].lower()
            or needle in c["code"].lower()
            or needle in (c.get("capital") or "").lower()
        ]
    total = len(items)
    start = (page - 1) * limit
    page_items = items[start : start + limit]
    data = [CountryOut.model_validate(_public(c)).model_dump() for c in page_items]
    return success(
        data,
        request_id=getattr(request.state, "request_id", None),
        page=page,
        limit=limit,
        total=total,
    )


@router.get("/{code}", summary="Get country by ISO code")
async def get_country(
    code: str,
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    if len(code) not in (2, 3):
        raise ValidationAppError(
            "Invalid country code. Expected ISO 3166-1 alpha-2 or alpha-3.",
            details={"example": "US"},
        )
    c = _find(code)
    if not c:
        raise NotFoundError(f"Country '{code.upper()}' not found")
    return success(
        CountryOut.model_validate(_public(c)).model_dump(),
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{code}/states", summary="List states/provinces for a country")
async def get_states(
    code: str,
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    c = _find(code)
    if not c:
        raise NotFoundError(f"Country '{code.upper()}' not found")
    states = [PlaceOut.model_validate(s).model_dump() for s in c.get("states") or []]
    return success(states, request_id=getattr(request.state, "request_id", None))


@router.get("/{code}/cities", summary="List sample cities for a country")
async def get_cities(
    code: str,
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    c = _find(code)
    if not c:
        raise NotFoundError(f"Country '{code.upper()}' not found")
    cities = [PlaceOut.model_validate(s).model_dump() for s in c.get("cities") or []]
    return success(cities, request_id=getattr(request.state, "request_id", None))
