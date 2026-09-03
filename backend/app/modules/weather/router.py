"""Weather provider abstraction and router."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.core.dependencies import optional_api_key
from app.core.exceptions import ProviderError, ValidationAppError
from app.core.responses import success

router = APIRouter(prefix="/weather", tags=["Weather"])


class WeatherCurrent(BaseModel):
    latitude: float
    longitude: float
    temperature: float
    feels_like: float | None = None
    humidity: float | None = None
    precipitation: float | None = None
    wind_speed: float | None = None
    wind_direction: float | None = None
    conditions: str
    sunrise: str | None = None
    sunset: str | None = None
    observed_at: str
    units: str = "metric"
    source: str


class ForecastDay(BaseModel):
    date: str
    temperature_max: float
    temperature_min: float
    precipitation: float | None = None
    conditions: str


class WeatherForecast(BaseModel):
    latitude: float
    longitude: float
    daily: list[ForecastDay]
    source: str


class WeatherHistorical(BaseModel):
    latitude: float
    longitude: float
    date: str
    temperature_max: float
    temperature_min: float
    precipitation: float | None = None
    conditions: str
    source: str
    note: str = Field(default="Historical values may be estimated in mock mode")


class WeatherProvider(ABC):
    @abstractmethod
    async def current(self, lat: float, lon: float) -> WeatherCurrent:
        ...

    @abstractmethod
    async def forecast(self, lat: float, lon: float, days: int = 7) -> WeatherForecast:
        ...

    @abstractmethod
    async def historical(self, lat: float, lon: float, date: str) -> WeatherHistorical:
        ...


class MockWeatherProvider(WeatherProvider):
    async def current(self, lat: float, lon: float) -> WeatherCurrent:
        return WeatherCurrent(
            latitude=lat,
            longitude=lon,
            temperature=18.5,
            feels_like=17.2,
            humidity=62,
            precipitation=0.0,
            wind_speed=12.4,
            wind_direction=220,
            conditions="Partly cloudy",
            sunrise="06:42",
            sunset="19:15",
            observed_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            source="mock",
        )

    async def forecast(self, lat: float, lon: float, days: int = 7) -> WeatherForecast:
        days = max(1, min(days, 14))
        base = datetime.now(timezone.utc).date()
        daily = []
        for i in range(days):
            d = base.fromordinal(base.toordinal() + i)
            daily.append(
                ForecastDay(
                    date=d.isoformat(),
                    temperature_max=20 + (i % 3),
                    temperature_min=10 + (i % 2),
                    precipitation=0.2 * i,
                    conditions="Clear" if i % 2 == 0 else "Cloudy",
                )
            )
        return WeatherForecast(latitude=lat, longitude=lon, daily=daily, source="mock")

    async def historical(self, lat: float, lon: float, date: str) -> WeatherHistorical:
        return WeatherHistorical(
            latitude=lat,
            longitude=lon,
            date=date,
            temperature_max=22.0,
            temperature_min=11.0,
            precipitation=1.5,
            conditions="Light rain",
            source="mock",
        )


class OpenMeteoProvider(WeatherProvider):
    BASE = "https://api.open-meteo.com/v1/forecast"

    async def current(self, lat: float, lon: float) -> WeatherCurrent:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
            "daily": "sunrise,sunset",
            "timezone": "UTC",
        }
        data = await self._get(params)
        cur = data.get("current") or {}
        daily = data.get("daily") or {}
        return WeatherCurrent(
            latitude=lat,
            longitude=lon,
            temperature=cur.get("temperature_2m"),
            feels_like=cur.get("apparent_temperature"),
            humidity=cur.get("relative_humidity_2m"),
            precipitation=cur.get("precipitation"),
            wind_speed=cur.get("wind_speed_10m"),
            wind_direction=cur.get("wind_direction_10m"),
            conditions=_wmo_code(cur.get("weather_code")),
            sunrise=(daily.get("sunrise") or [None])[0],
            sunset=(daily.get("sunset") or [None])[0],
            observed_at=cur.get("time") or datetime.now(timezone.utc).isoformat(),
            source="openmeteo",
        )

    async def forecast(self, lat: float, lon: float, days: int = 7) -> WeatherForecast:
        days = max(1, min(days, 14))
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
            "forecast_days": days,
            "timezone": "UTC",
        }
        data = await self._get(params)
        daily = data.get("daily") or {}
        out = []
        dates = daily.get("time") or []
        for i, date in enumerate(dates):
            out.append(
                ForecastDay(
                    date=date,
                    temperature_max=(daily.get("temperature_2m_max") or [None])[i],
                    temperature_min=(daily.get("temperature_2m_min") or [None])[i],
                    precipitation=(daily.get("precipitation_sum") or [None])[i],
                    conditions=_wmo_code((daily.get("weather_code") or [None])[i]),
                )
            )
        return WeatherForecast(latitude=lat, longitude=lon, daily=out, source="openmeteo")

    async def historical(self, lat: float, lon: float, date: str) -> WeatherHistorical:
        # Open-Meteo archive API
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": date,
            "end_date": date,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
            "timezone": "UTC",
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                r = await client.get(url, params=params)
                r.raise_for_status()
            except httpx.HTTPError as exc:
                raise ProviderError("Open-Meteo historical request failed") from exc
            data = r.json()
        daily = data.get("daily") or {}
        return WeatherHistorical(
            latitude=lat,
            longitude=lon,
            date=date,
            temperature_max=(daily.get("temperature_2m_max") or [0])[0],
            temperature_min=(daily.get("temperature_2m_min") or [0])[0],
            precipitation=(daily.get("precipitation_sum") or [None])[0],
            conditions=_wmo_code((daily.get("weather_code") or [0])[0]),
            source="openmeteo",
            note="From Open-Meteo archive",
        )

    async def _get(self, params: dict) -> dict:
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                r = await client.get(self.BASE, params=params)
                r.raise_for_status()
                return r.json()
            except httpx.HTTPError as exc:
                raise ProviderError("Open-Meteo request failed") from exc


def _wmo_code(code: int | None) -> str:
    mapping = {
        0: "Clear",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        61: "Light rain",
        63: "Rain",
        71: "Snow",
        95: "Thunderstorm",
    }
    if code is None:
        return "Unknown"
    return mapping.get(int(code), f"Code {code}")


def get_weather_provider() -> WeatherProvider:
    s = get_settings()
    if s.mock_mode or s.weather_provider == "mock":
        return MockWeatherProvider()
    return OpenMeteoProvider()


@router.get("", summary="Current weather")
async def current_weather(
    request: Request,
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    data = await get_weather_provider().current(lat, lon)
    return success(data.model_dump(), request_id=getattr(request.state, "request_id", None))


@router.get("/forecast", summary="Weather forecast")
async def forecast_weather(
    request: Request,
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    days: int = Query(7, ge=1, le=14),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    data = await get_weather_provider().forecast(lat, lon, days=days)
    return success(data.model_dump(), request_id=getattr(request.state, "request_id", None))


@router.get("/historical", summary="Historical weather for a date")
async def historical_weather(
    request: Request,
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    date: str = Query(..., description="YYYY-MM-DD"),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationAppError(
            "Invalid date. Expected YYYY-MM-DD.", details={"example": "2024-01-15"}
        ) from exc
    data = await get_weather_provider().historical(lat, lon, date)
    return success(data.model_dump(), request_id=getattr(request.state, "request_id", None))
