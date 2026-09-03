"""Country schemas and mock data."""

from __future__ import annotations

from pydantic import BaseModel, Field


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


MOCK_COUNTRIES: list[dict] = [
    {
        "code": "US",
        "code3": "USA",
        "name": "United States",
        "official_name": "United States of America",
        "capital": "Washington, D.C.",
        "region": "Americas",
        "subregion": "North America",
        "continent": "North America",
        "latitude": 38.0,
        "longitude": -97.0,
        "currencies": [{"code": "USD", "name": "United States dollar", "symbol": "$"}],
        "languages": ["English"],
        "timezones": ["UTC-12:00", "UTC-05:00", "UTC-04:00"],
        "states": [
            {"name": "California", "code": "CA"},
            {"name": "New York", "code": "NY"},
            {"name": "Pennsylvania", "code": "PA"},
            {"name": "Texas", "code": "TX"},
        ],
        "cities": [
            {"name": "New York"},
            {"name": "Los Angeles"},
            {"name": "Chicago"},
            {"name": "Pittsburgh"},
        ],
    },
    {
        "code": "GB",
        "code3": "GBR",
        "name": "United Kingdom",
        "official_name": "United Kingdom of Great Britain and Northern Ireland",
        "capital": "London",
        "region": "Europe",
        "subregion": "Northern Europe",
        "continent": "Europe",
        "latitude": 54.0,
        "longitude": -2.0,
        "currencies": [{"code": "GBP", "name": "British pound", "symbol": "£"}],
        "languages": ["English"],
        "timezones": ["UTC"],
        "states": [
            {"name": "England", "code": "ENG"},
            {"name": "Scotland", "code": "SCT"},
        ],
        "cities": [{"name": "London"}, {"name": "Manchester"}, {"name": "Edinburgh"}],
    },
    {
        "code": "IN",
        "code3": "IND",
        "name": "India",
        "official_name": "Republic of India",
        "capital": "New Delhi",
        "region": "Asia",
        "subregion": "Southern Asia",
        "continent": "Asia",
        "latitude": 20.0,
        "longitude": 77.0,
        "currencies": [{"code": "INR", "name": "Indian rupee", "symbol": "₹"}],
        "languages": ["Hindi", "English"],
        "timezones": ["UTC+05:30"],
        "states": [
            {"name": "Maharashtra", "code": "MH"},
            {"name": "Karnataka", "code": "KA"},
        ],
        "cities": [{"name": "Mumbai"}, {"name": "Bengaluru"}, {"name": "Delhi"}],
    },
    {
        "code": "DE",
        "code3": "DEU",
        "name": "Germany",
        "official_name": "Federal Republic of Germany",
        "capital": "Berlin",
        "region": "Europe",
        "subregion": "Western Europe",
        "continent": "Europe",
        "latitude": 51.0,
        "longitude": 9.0,
        "currencies": [{"code": "EUR", "name": "Euro", "symbol": "€"}],
        "languages": ["German"],
        "timezones": ["UTC+01:00"],
        "states": [{"name": "Bavaria", "code": "BY"}],
        "cities": [{"name": "Berlin"}, {"name": "Munich"}, {"name": "Hamburg"}],
    },
    {
        "code": "JP",
        "code3": "JPN",
        "name": "Japan",
        "official_name": "Japan",
        "capital": "Tokyo",
        "region": "Asia",
        "subregion": "Eastern Asia",
        "continent": "Asia",
        "latitude": 36.0,
        "longitude": 138.0,
        "currencies": [{"code": "JPY", "name": "Japanese yen", "symbol": "¥"}],
        "languages": ["Japanese"],
        "timezones": ["UTC+09:00"],
        "states": [{"name": "Tokyo", "code": "13"}],
        "cities": [{"name": "Tokyo"}, {"name": "Osaka"}, {"name": "Kyoto"}],
    },
    {
        "code": "BR",
        "code3": "BRA",
        "name": "Brazil",
        "official_name": "Federative Republic of Brazil",
        "capital": "Brasília",
        "region": "Americas",
        "subregion": "South America",
        "continent": "South America",
        "latitude": -10.0,
        "longitude": -55.0,
        "currencies": [{"code": "BRL", "name": "Brazilian real", "symbol": "R$"}],
        "languages": ["Portuguese"],
        "timezones": ["UTC-05:00", "UTC-03:00"],
        "states": [{"name": "São Paulo", "code": "SP"}],
        "cities": [{"name": "São Paulo"}, {"name": "Rio de Janeiro"}],
    },
    {
        "code": "AU",
        "code3": "AUS",
        "name": "Australia",
        "official_name": "Commonwealth of Australia",
        "capital": "Canberra",
        "region": "Oceania",
        "subregion": "Australia and New Zealand",
        "continent": "Oceania",
        "latitude": -27.0,
        "longitude": 133.0,
        "currencies": [{"code": "AUD", "name": "Australian dollar", "symbol": "$"}],
        "languages": ["English"],
        "timezones": ["UTC+08:00", "UTC+10:00", "UTC+11:00"],
        "states": [{"name": "New South Wales", "code": "NSW"}],
        "cities": [{"name": "Sydney"}, {"name": "Melbourne"}, {"name": "Canberra"}],
    },
    {
        "code": "CA",
        "code3": "CAN",
        "name": "Canada",
        "official_name": "Canada",
        "capital": "Ottawa",
        "region": "Americas",
        "subregion": "North America",
        "continent": "North America",
        "latitude": 60.0,
        "longitude": -95.0,
        "currencies": [{"code": "CAD", "name": "Canadian dollar", "symbol": "$"}],
        "languages": ["English", "French"],
        "timezones": ["UTC-08:00", "UTC-05:00", "UTC-03:30"],
        "states": [{"name": "Ontario", "code": "ON"}, {"name": "Quebec", "code": "QC"}],
        "cities": [{"name": "Toronto"}, {"name": "Montreal"}, {"name": "Vancouver"}],
    },
]
