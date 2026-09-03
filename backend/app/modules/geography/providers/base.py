"""Geography provider abstraction."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod

import httpx

from app.core.exceptions import NotFoundError, ProviderError, ValidationAppError
from app.modules.geography.schemas import DistanceResult, GeocodeResult, GeoPoint

DEMO_PLACES: dict[str, GeocodeResult] = {
    "pittsburgh": GeocodeResult(
        display_name="Pittsburgh, Pennsylvania, United States",
        latitude=40.4406,
        longitude=-79.9959,
        country="United States",
        country_code="US",
        city="Pittsburgh",
        state="Pennsylvania",
        source="mock",
    ),
    "carnegie mellon university": GeocodeResult(
        display_name="Carnegie Mellon University, Pittsburgh, PA, USA",
        latitude=40.4433,
        longitude=-79.9436,
        country="United States",
        country_code="US",
        city="Pittsburgh",
        state="Pennsylvania",
        source="mock",
    ),
    "london": GeocodeResult(
        display_name="London, England, United Kingdom",
        latitude=51.5074,
        longitude=-0.1278,
        country="United Kingdom",
        country_code="GB",
        city="London",
        state="England",
        source="mock",
    ),
    "tokyo": GeocodeResult(
        display_name="Tokyo, Japan",
        latitude=35.6762,
        longitude=139.6503,
        country="Japan",
        country_code="JP",
        city="Tokyo",
        source="mock",
    ),
    "mumbai": GeocodeResult(
        display_name="Mumbai, Maharashtra, India",
        latitude=19.0760,
        longitude=72.8777,
        country="India",
        country_code="IN",
        city="Mumbai",
        state="Maharashtra",
        source="mock",
    ),
}


class GeographyProvider(ABC):
    @abstractmethod
    async def geocode(self, query: str) -> list[GeocodeResult]:
        ...

    @abstractmethod
    async def reverse_geocode(self, latitude: float, longitude: float) -> GeocodeResult:
        ...


class DemoProvider(GeographyProvider):
    async def geocode(self, query: str) -> list[GeocodeResult]:
        q = query.strip().lower()
        if q in DEMO_PLACES:
            return [DEMO_PLACES[q]]
        matches = [v for k, v in DEMO_PLACES.items() if q in k]
        if not matches:
            raise NotFoundError(f"No geocoding results for '{query}' (mock dataset)")
        return matches

    async def reverse_geocode(self, latitude: float, longitude: float) -> GeocodeResult:
        best = None
        best_d = float("inf")
        for place in DEMO_PLACES.values():
            d = haversine_km(latitude, longitude, place.latitude, place.longitude)
            if d < best_d:
                best_d = d
                best = place
        if best is None or best_d > 500:
            raise NotFoundError("No reverse geocode match in mock dataset")
        return best


class OpenStreetMapProvider(GeographyProvider):
    BASE = "https://nominatim.openstreetmap.org"

    async def geocode(self, query: str) -> list[GeocodeResult]:
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                r = await client.get(
                    f"{self.BASE}/search",
                    params={"q": query, "format": "json", "addressdetails": 1, "limit": 5},
                    headers={"User-Agent": "StudentAPIPlatform/0.1 (open-source education)"},
                )
                r.raise_for_status()
            except httpx.HTTPError as exc:
                raise ProviderError("Nominatim geocode failed") from exc
        data = r.json()
        if not data:
            raise NotFoundError(f"No geocoding results for '{query}'")
        return [self._normalize(item) for item in data]

    async def reverse_geocode(self, latitude: float, longitude: float) -> GeocodeResult:
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                r = await client.get(
                    f"{self.BASE}/reverse",
                    params={
                        "lat": latitude,
                        "lon": longitude,
                        "format": "json",
                        "addressdetails": 1,
                    },
                    headers={"User-Agent": "StudentAPIPlatform/0.1 (open-source education)"},
                )
                r.raise_for_status()
            except httpx.HTTPError as exc:
                raise ProviderError("Nominatim reverse geocode failed") from exc
        data = r.json()
        if not data or "error" in data:
            raise NotFoundError("No reverse geocode result")
        return self._normalize(data)

    @staticmethod
    def _normalize(item: dict) -> GeocodeResult:
        addr = item.get("address") or {}
        return GeocodeResult(
            display_name=item.get("display_name") or "",
            latitude=float(item["lat"]),
            longitude=float(item["lon"]),
            country=addr.get("country"),
            country_code=(addr.get("country_code") or "").upper() or None,
            city=addr.get("city") or addr.get("town") or addr.get("village"),
            state=addr.get("state"),
            source="nominatim",
        )


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def compute_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> DistanceResult:
    for v, name in [
        (lat1, "from_lat"),
        (lat2, "to_lat"),
    ]:
        if not -90 <= v <= 90:
            raise ValidationAppError(f"Invalid latitude for {name}")
    for v, name in [
        (lon1, "from_lon"),
        (lon2, "to_lon"),
    ]:
        if not -180 <= v <= 180:
            raise ValidationAppError(f"Invalid longitude for {name}")
    km = haversine_km(lat1, lon1, lat2, lon2)
    return DistanceResult(
        from_point=GeoPoint(latitude=lat1, longitude=lon1),
        to_point=GeoPoint(latitude=lat2, longitude=lon2),
        distance_km=round(km, 3),
        distance_miles=round(km * 0.621371, 3),
    )


def get_geography_provider(*, mock_mode: bool, provider_name: str) -> GeographyProvider:
    if mock_mode or provider_name == "demo":
        return DemoProvider()
    return OpenStreetMapProvider()
