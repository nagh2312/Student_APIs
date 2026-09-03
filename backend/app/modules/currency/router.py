"""Currency API — Frankfurter + mock."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.core.dependencies import optional_api_key
from app.core.exceptions import NotFoundError, ProviderError, ValidationAppError
from app.core.responses import success

router = APIRouter(tags=["Currency"])

COMMON_CURRENCIES = [
    {"code": "USD", "name": "United States Dollar"},
    {"code": "EUR", "name": "Euro"},
    {"code": "GBP", "name": "British Pound"},
    {"code": "JPY", "name": "Japanese Yen"},
    {"code": "INR", "name": "Indian Rupee"},
    {"code": "CAD", "name": "Canadian Dollar"},
    {"code": "AUD", "name": "Australian Dollar"},
    {"code": "CHF", "name": "Swiss Franc"},
    {"code": "CNY", "name": "Chinese Yuan"},
    {"code": "BRL", "name": "Brazilian Real"},
    {"code": "MXN", "name": "Mexican Peso"},
    {"code": "KRW", "name": "South Korean Won"},
    {"code": "SGD", "name": "Singapore Dollar"},
    {"code": "NZD", "name": "New Zealand Dollar"},
    {"code": "SEK", "name": "Swedish Krona"},
    {"code": "NOK", "name": "Norwegian Krone"},
    {"code": "DKK", "name": "Danish Krone"},
    {"code": "ZAR", "name": "South African Rand"},
    {"code": "HKD", "name": "Hong Kong Dollar"},
    {"code": "AED", "name": "UAE Dirham"},
]

# Deterministic mock FX rates vs USD (educational demo — not live market data)
MOCK_RATES_USD = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 149.5,
    "INR": 83.2,
    "CAD": 1.36,
    "AUD": 1.52,
    "CHF": 0.88,
    "CNY": 7.24,
    "BRL": 5.05,
    "MXN": 17.1,
    "KRW": 1330.0,
    "SGD": 1.34,
    "NZD": 1.64,
    "SEK": 10.5,
    "NOK": 10.8,
    "DKK": 6.86,
    "ZAR": 18.7,
    "HKD": 7.82,
    "AED": 3.67,
}


class CurrencyInfo(BaseModel):
    code: str
    name: str


class RatesOut(BaseModel):
    base: str
    date: str
    rates: dict[str, float]
    source: str
    kind: str = Field(description="current | historical")


class ConvertOut(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    rate: float
    converted_amount: float
    timestamp: str
    source: str
    kind: str = "current"


class CurrencyProvider(ABC):
    @abstractmethod
    async def currencies(self) -> list[CurrencyInfo]:
        ...

    @abstractmethod
    async def rates(self, base: str = "USD", date: str | None = None) -> RatesOut:
        ...

    @abstractmethod
    async def convert(
        self, from_currency: str, to_currency: str, amount: float
    ) -> ConvertOut:
        ...


class MockCurrencyProvider(CurrencyProvider):
    async def currencies(self) -> list[CurrencyInfo]:
        return [CurrencyInfo(**c) for c in COMMON_CURRENCIES]

    async def rates(self, base: str = "USD", date: str | None = None) -> RatesOut:
        base = base.upper()
        if base not in MOCK_RATES_USD and base != "USD":
            # convert via USD
            if base not in MOCK_RATES_USD:
                raise NotFoundError(f"Unknown currency '{base}'")
        usd_rates = dict(MOCK_RATES_USD)
        if base == "USD":
            rates = {k: v for k, v in usd_rates.items() if k != "USD"}
        else:
            base_to_usd = 1.0 / usd_rates[base]
            rates = {
                k: round(base_to_usd * v, 6)
                for k, v in usd_rates.items()
                if k != base
            }
        return RatesOut(
            base=base,
            date=date or datetime.now(timezone.utc).date().isoformat(),
            rates=rates,
            source="mock",
            kind="historical" if date else "current",
        )

    async def convert(self, from_currency: str, to_currency: str, amount: float):
        from_currency, to_currency = from_currency.upper(), to_currency.upper()
        rates = await self.rates(base=from_currency)
        if from_currency == to_currency:
            rate = 1.0
        elif to_currency not in rates.rates:
            raise NotFoundError(f"Unknown currency '{to_currency}'")
        else:
            rate = rates.rates[to_currency]
        return ConvertOut(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            rate=rate,
            converted_amount=round(amount * rate, 6),
            timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            source="mock",
        )


class FrankfurterProvider(CurrencyProvider):
    BASE = "https://api.frankfurter.app"

    async def currencies(self) -> list[CurrencyInfo]:
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                r = await client.get(f"{self.BASE}/currencies")
                r.raise_for_status()
                data = r.json()
            except httpx.HTTPError as exc:
                raise ProviderError("Frankfurter currencies failed") from exc
        return [CurrencyInfo(code=k, name=v) for k, v in data.items()]

    async def rates(self, base: str = "USD", date: str | None = None) -> RatesOut:
        path = f"/{date}" if date else "/latest"
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                r = await client.get(f"{self.BASE}{path}", params={"from": base.upper()})
                if r.status_code == 404:
                    raise NotFoundError(f"Rates not found for base '{base}'")
                r.raise_for_status()
                data = r.json()
            except NotFoundError:
                raise
            except httpx.HTTPError as exc:
                raise ProviderError("Frankfurter rates failed") from exc
        return RatesOut(
            base=data.get("base", base.upper()),
            date=data.get("date", ""),
            rates=data.get("rates") or {},
            source="frankfurter",
            kind="historical" if date else "current",
        )

    async def convert(self, from_currency: str, to_currency: str, amount: float):
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                r = await client.get(
                    f"{self.BASE}/latest",
                    params={
                        "amount": amount,
                        "from": from_currency.upper(),
                        "to": to_currency.upper(),
                    },
                )
                r.raise_for_status()
                data = r.json()
            except httpx.HTTPError as exc:
                raise ProviderError("Frankfurter convert failed") from exc
        rate = list((data.get("rates") or {}).values())[0]
        return ConvertOut(
            from_currency=from_currency.upper(),
            to_currency=to_currency.upper(),
            amount=amount,
            rate=rate,
            converted_amount=round(float(rate), 6)
            if amount == 1
            else round(float(list(data["rates"].values())[0]), 6),
            timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            source="frankfurter",
        )


def get_currency_provider() -> CurrencyProvider:
    s = get_settings()
    if s.mock_mode or s.currency_provider == "mock":
        return MockCurrencyProvider()
    return FrankfurterProvider()


@router.get("/currencies", summary="List supported currencies")
async def list_currencies(
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    data = await get_currency_provider().currencies()
    return success(
        [c.model_dump() for c in data],
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/rates", summary="Latest FX rates (default base USD)")
@router.get("/rates/{base}", summary="Latest FX rates for a base currency")
async def get_rates(
    request: Request,
    base: str = "USD",
    date: str | None = Query(None, description="Optional historical date YYYY-MM-DD"),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    data = await get_currency_provider().rates(base=base, date=date)
    return success(data.model_dump(), request_id=getattr(request.state, "request_id", None))


@router.get("/convert", summary="Convert amount between currencies")
async def convert(
    request: Request,
    amount: float = Query(..., gt=0),
    from_currency: str = Query(..., alias="from", min_length=3, max_length=3),
    to_currency: str = Query(..., alias="to", min_length=3, max_length=3),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    if len(from_currency) != 3 or len(to_currency) != 3:
        raise ValidationAppError("Currency codes must be 3-letter ISO 4217 codes.")
    data = await get_currency_provider().convert(from_currency, to_currency, amount)
    return success(data.model_dump(), request_id=getattr(request.state, "request_id", None))
