"""Time and timezone utilities (IANA via zoneinfo)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from zoneinfo import ZoneInfo, available_timezones

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel

from app.core.dependencies import optional_api_key
from app.core.exceptions import NotFoundError, ValidationAppError
from app.core.responses import success

router = APIRouter(tags=["Time"])


class TimeOut(BaseModel):
    timezone: str
    datetime: str
    utc_offset: str
    unix: int
    day_of_week: str
    is_dst: bool


class ConvertOut(BaseModel):
    from_timezone: str
    to_timezone: str
    from_datetime: str
    to_datetime: str
    unix: int


def _safe_tz(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except Exception as exc:
        raise NotFoundError(
            f"Unknown timezone '{name}'. Use IANA names like America/New_York."
        ) from exc


def _format(dt: datetime, tz_name: str) -> TimeOut:
    offset = dt.utcoffset() or timezone.utc.utcoffset(dt)  # type: ignore
    total = int(offset.total_seconds()) if offset else 0
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    hh, mm = divmod(total // 60, 60)
    return TimeOut(
        timezone=tz_name,
        datetime=dt.isoformat(),
        utc_offset=f"{sign}{hh:02d}:{mm:02d}",
        unix=int(dt.timestamp()),
        day_of_week=dt.strftime("%A"),
        is_dst=bool(dt.dst()),
    )


@router.get("/time", summary="Current UTC time")
async def current_utc(
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    now = datetime.now(timezone.utc)
    return success(
        _format(now, "UTC").model_dump(),
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/time/convert", summary="Convert time between timezones")
async def convert_time(
    request: Request,
    from_tz: str = Query(..., alias="from", description="Source IANA timezone"),
    to_tz: str = Query(..., alias="to", description="Target IANA timezone"),
    at: str | None = Query(
        None, description="Optional ISO datetime in source tz; default now"
    ),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    src = _safe_tz(from_tz)
    dst = _safe_tz(to_tz)
    if at:
        try:
            dt = datetime.fromisoformat(at.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=src)
            else:
                dt = dt.astimezone(src)
        except ValueError as exc:
            raise ValidationAppError(
                "Invalid datetime. Use ISO 8601.", details={"example": "2026-09-02T15:00:00"}
            ) from exc
    else:
        dt = datetime.now(src)
    converted = dt.astimezone(dst)
    out = ConvertOut(
        from_timezone=from_tz,
        to_timezone=to_tz,
        from_datetime=dt.isoformat(),
        to_datetime=converted.isoformat(),
        unix=int(dt.timestamp()),
    )
    return success(out.model_dump(), request_id=getattr(request.state, "request_id", None))


@router.get("/time/{tz:path}", summary="Current time in a timezone")
async def time_in_zone(
    tz: str,
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    zone = _safe_tz(tz)
    now = datetime.now(zone)
    return success(
        _format(now, tz).model_dump(),
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/timezones", summary="List IANA timezones")
async def list_timezones(
    request: Request,
    q: str | None = Query(None, description="Filter substring"),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    zones = sorted(available_timezones())
    if q:
        needle = q.lower()
        zones = [z for z in zones if needle in z.lower()]
    return success(zones, request_id=getattr(request.state, "request_id", None))
