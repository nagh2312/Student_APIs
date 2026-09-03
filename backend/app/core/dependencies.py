"""Shared FastAPI dependencies."""

from __future__ import annotations

from typing import Annotated, AsyncGenerator
from uuid import uuid4

from fastapi import Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings


async def get_db() -> AsyncGenerator[AsyncSession | None, None]:
    """Yield a DB session, or None when MOCK_MODE is enabled."""
    settings = get_settings()
    if settings.mock_mode:
        yield None
        return
    from app.database.connection import get_session_factory

    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", str(uuid4()))


def get_redis(request: Request):
    return getattr(request.app.state, "redis", None)


SettingsDep = Annotated[Settings, Depends(get_settings)]
DbDep = Annotated[AsyncSession | None, Depends(get_db)]
RequestIdDep = Annotated[str, Depends(get_request_id)]


async def optional_api_key(
    request: Request,
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> str | None:
    request.state.api_key = x_api_key
    request.state.authenticated = bool(x_api_key)
    return x_api_key
