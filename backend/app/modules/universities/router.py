"""Universities API router."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.dependencies import get_db, optional_api_key
from app.core.responses import success
from app.modules.universities.service import UniversityService

router = APIRouter(prefix="/universities", tags=["Universities"])


def _service(session: AsyncSession | None) -> UniversityService:
    settings = get_settings()
    return UniversityService(session, mock_mode=settings.mock_mode)


@router.get(
    "",
    summary="List universities",
    description="Search and filter universities. Supports pagination and sorting.",
)
async def list_universities(
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    country: str | None = Query(None, description="ISO country code or name, e.g. US"),
    name: str | None = Query(None, description="Substring match on university name"),
    q: str | None = Query(None, description="General search across name, country, city"),
    sort: str = Query("name", description="Sort field; prefix with - for descending"),
    session: AsyncSession | None = Depends(get_db),
):
    settings = get_settings()
    svc = _service(session if not settings.mock_mode else None)
    data, total, page, limit = await svc.list_universities(
        page=page, limit=limit, country=country, name=name, q=q, sort=sort
    )
    return success(
        [d.model_dump() for d in data],
        request_id=getattr(request.state, "request_id", None),
        page=page,
        limit=limit,
        total=total,
    )


@router.get("/{university_id}", summary="Get university by ID")
async def get_university(
    university_id: str,
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
    session: AsyncSession | None = Depends(get_db),
):
    settings = get_settings()
    svc = _service(session if not settings.mock_mode else None)
    uni = await svc.get_university(university_id)
    return success(
        uni.model_dump(),
        request_id=getattr(request.state, "request_id", None),
    )


@router.get("/{university_id}/programs", summary="List programs for a university")
async def get_programs(
    university_id: str,
    request: Request,
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
    session: AsyncSession | None = Depends(get_db),
):
    settings = get_settings()
    svc = _service(session if not settings.mock_mode else None)
    programs = await svc.get_programs(university_id)
    return success(
        [p.model_dump() for p in programs],
        request_id=getattr(request.state, "request_id", None),
    )
