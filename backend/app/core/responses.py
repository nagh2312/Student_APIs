"""Standard API response envelope and pagination helpers."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorBody(BaseModel):
    code: str
    message: str
    details: Any = None
    request_id: str | None = None


class PaginationMeta(BaseModel):
    page: int = 1
    limit: int = 20
    total: int = 0
    has_next: bool = False
    has_prev: bool = False
    request_id: str | None = None


class Meta(BaseModel):
    request_id: str | None = None
    page: int | None = None
    limit: int | None = None
    total: int | None = None
    has_next: bool | None = None
    has_prev: bool | None = None


class APIResponse(BaseModel, Generic[T]):
    data: T | None = None
    meta: dict[str, Any] | Meta = Field(default_factory=dict)
    error: ErrorBody | None = None


def success(
    data: Any,
    *,
    request_id: str | None = None,
    page: int | None = None,
    limit: int | None = None,
    total: int | None = None,
    extra_meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    meta: dict[str, Any] = {"request_id": request_id}
    if page is not None:
        meta["page"] = page
        meta["limit"] = limit
        meta["total"] = total or 0
        meta["has_next"] = bool(
            page is not None
            and limit is not None
            and total is not None
            and page * limit < total
        )
        meta["has_prev"] = bool(page and page > 1)
    if extra_meta:
        meta.update(extra_meta)
    return {"data": data, "meta": meta, "error": None}


def failure(
    *,
    code: str,
    message: str,
    request_id: str | None = None,
    details: Any = None,
) -> dict[str, Any]:
    return {
        "data": None,
        "meta": {"request_id": request_id},
        "error": {
            "code": code,
            "message": message,
            "details": details,
            "request_id": request_id,
        },
    }


def clamp_pagination(page: int, limit: int, max_limit: int = 100) -> tuple[int, int]:
    page = max(1, page)
    limit = max(1, min(limit, max_limit))
    return page, limit
