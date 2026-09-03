"""Geography schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class GeoPoint(BaseModel):
    latitude: float
    longitude: float


class GeocodeResult(BaseModel):
    display_name: str
    latitude: float
    longitude: float
    country: str | None = None
    country_code: str | None = None
    city: str | None = None
    state: str | None = None
    source: str = Field(description="Provider used: mock | nominatim")


class DistanceResult(BaseModel):
    from_point: GeoPoint
    to_point: GeoPoint
    distance_km: float
    distance_miles: float
    method: str = "haversine"
