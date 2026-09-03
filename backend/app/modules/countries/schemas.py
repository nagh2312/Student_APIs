"""Country Pydantic schemas and seed loader."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.data import countries as load_countries


class CountryOut(BaseModel):
    code: str = Field(..., min_length=2, max_length=2)
    code3: str
    name: str
    official_name: str | None = None
    capital: str | None = None
    region: str | None = None
    subregion: str | None = None
    continent: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    currencies: list[dict] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    timezones: list[str] = Field(default_factory=list)


class PlaceOut(BaseModel):
    name: str
    code: str | None = None


# ~250 countries from mledoze/countries (see docs/DATA-SOURCES.md)
MOCK_COUNTRIES: list[dict] = load_countries()
