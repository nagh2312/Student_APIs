"""University Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl


class UniversityOut(BaseModel):
    id: str
    name: str
    country: str
    country_code: str = Field(..., min_length=2, max_length=2)
    state: str | None = None
    city: str | None = None
    website: str | None = None
    domains: list[str] = Field(default_factory=list)


class ProgramOut(BaseModel):
    id: str
    name: str
    level: str | None = None
    department: str | None = None
