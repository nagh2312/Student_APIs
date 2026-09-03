"""Aggregate v1 API routers."""

from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.books.router import router as books_router
from app.modules.catalog import router as catalog_router
from app.modules.countries.router import router as countries_router
from app.modules.currency.router import router as currency_router
from app.modules.geography.router import router as geography_router
from app.modules.time.router import router as time_router
from app.modules.universities.router import router as universities_router
from app.modules.weather.router import router as weather_router

api_v1_router = APIRouter()
api_v1_router.include_router(catalog_router)
api_v1_router.include_router(universities_router)
api_v1_router.include_router(countries_router)
api_v1_router.include_router(geography_router)
api_v1_router.include_router(weather_router)
api_v1_router.include_router(books_router)
api_v1_router.include_router(currency_router)
api_v1_router.include_router(time_router)
api_v1_router.include_router(auth_router)
