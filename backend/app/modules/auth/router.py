"""API key management (hashed at rest)."""

from __future__ import annotations

import secrets
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.dependencies import get_db, optional_api_key
from app.core.exceptions import NotFoundError
from app.core.responses import success
from app.core.security import generate_api_key, hash_api_key
from app.modules.auth.models import APIKey

router = APIRouter(prefix="/auth/api-keys", tags=["Auth"])

# In-memory store for mock / when DB unavailable
_MEMORY_KEYS: dict[str, dict] = {}


class CreateKeyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    owner_email: EmailStr | None = None
    notes: str | None = None


class KeyOut(BaseModel):
    id: str
    name: str
    key_prefix: str
    owner_email: str | None = None
    created_at: str
    raw_key: str | None = Field(
        default=None, description="Only returned once at creation"
    )


@router.post("", summary="Create an API key", status_code=201)
async def create_key(
    body: CreateKeyRequest,
    request: Request,
    session: AsyncSession | None = Depends(get_db),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    settings = get_settings()
    raw = generate_api_key()
    key_id = secrets.token_hex(8)
    prefix = raw[:8]
    created = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    record = {
        "id": key_id,
        "name": body.name,
        "key_hash": hash_api_key(raw),
        "key_prefix": prefix,
        "owner_email": body.owner_email,
        "created_at": created,
        "is_active": True,
    }

    if settings.mock_mode:
        _MEMORY_KEYS[key_id] = record
    else:
        row = APIKey(
            id=key_id,
            name=body.name,
            key_hash=record["key_hash"],
            key_prefix=prefix,
            owner_email=str(body.owner_email) if body.owner_email else None,
            notes=body.notes,
        )
        session.add(row)
        await session.flush()

    out = KeyOut(
        id=key_id,
        name=body.name,
        key_prefix=prefix,
        owner_email=str(body.owner_email) if body.owner_email else None,
        created_at=created,
        raw_key=raw,
    )
    return success(out.model_dump(), request_id=getattr(request.state, "request_id", None))


@router.get("", summary="List API key metadata (no raw secrets)")
async def list_keys(
    request: Request,
    session: AsyncSession | None = Depends(get_db),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    settings = get_settings()
    if settings.mock_mode:
        items = [
            {
                "id": v["id"],
                "name": v["name"],
                "key_prefix": v["key_prefix"],
                "owner_email": v.get("owner_email"),
                "created_at": v["created_at"],
                "raw_key": None,
            }
            for v in _MEMORY_KEYS.values()
            if v.get("is_active")
        ]
    else:
        rows = (await session.scalars(select(APIKey).where(APIKey.is_active.is_(True)))).all()
        items = [
            {
                "id": r.id,
                "name": r.name,
                "key_prefix": r.key_prefix,
                "owner_email": r.owner_email,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "raw_key": None,
            }
            for r in rows
        ]
    return success(items, request_id=getattr(request.state, "request_id", None))


@router.delete("/{key_id}", summary="Revoke an API key", status_code=200)
async def delete_key(
    key_id: str,
    request: Request,
    session: AsyncSession | None = Depends(get_db),
    _auth: Annotated[str | None, Depends(optional_api_key)] = None,
):
    settings = get_settings()
    if settings.mock_mode:
        if key_id not in _MEMORY_KEYS:
            raise NotFoundError(f"API key '{key_id}' not found")
        _MEMORY_KEYS[key_id]["is_active"] = False
    else:
        row = await session.get(APIKey, key_id)
        if not row or not row.is_active:
            raise NotFoundError(f"API key '{key_id}' not found")
        row.is_active = False
        row.revoked_at = datetime.now(timezone.utc)
    return success(
        {"id": key_id, "revoked": True},
        request_id=getattr(request.state, "request_id", None),
    )
