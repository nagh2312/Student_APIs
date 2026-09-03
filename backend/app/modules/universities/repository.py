"""University repository — DB or in-memory mock."""

from __future__ import annotations

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.universities.mock_data import MOCK_UNIVERSITIES
from app.modules.universities.models import University


def _filter_mock(
    *,
    country: str | None,
    name: str | None,
    q: str | None,
    sort: str,
) -> list[dict]:
    items = list(MOCK_UNIVERSITIES)
    if country:
        code = country.upper()
        items = [
            u
            for u in items
            if u["country_code"] == code or u["country"].lower() == country.lower()
        ]
    if name:
        needle = name.lower()
        items = [u for u in items if needle in u["name"].lower()]
    if q:
        needle = q.lower()
        items = [
            u
            for u in items
            if needle in u["name"].lower()
            or needle in u["country"].lower()
            or needle in (u.get("city") or "").lower()
        ]
    reverse = sort.startswith("-")
    key = sort.lstrip("-")
    if key not in {"name", "country", "country_code"}:
        key = "name"
    items.sort(key=lambda u: (u.get(key) or ""), reverse=reverse)
    return items


class UniversityRepository:
    def __init__(self, session: AsyncSession | None, mock_mode: bool):
        self.session = session
        self.mock_mode = mock_mode

    async def list(
        self,
        *,
        page: int,
        limit: int,
        country: str | None = None,
        name: str | None = None,
        q: str | None = None,
        sort: str = "name",
    ) -> tuple[list[dict], int]:
        if self.mock_mode or self.session is None:
            items = _filter_mock(country=country, name=name, q=q, sort=sort)
            total = len(items)
            start = (page - 1) * limit
            return items[start : start + limit], total

        stmt = select(University)
        if country:
            code = country.upper()
            stmt = stmt.where(
                or_(
                    University.country_code == code,
                    func.lower(University.country) == country.lower(),
                )
            )
        if name:
            stmt = stmt.where(University.name.ilike(f"%{name}%"))
        if q:
            stmt = stmt.where(
                or_(
                    University.name.ilike(f"%{q}%"),
                    University.country.ilike(f"%{q}%"),
                    University.city.ilike(f"%{q}%"),
                )
            )
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = int(await self.session.scalar(count_stmt) or 0)

        reverse = sort.startswith("-")
        key = sort.lstrip("-")
        col = getattr(University, key, University.name)
        stmt = stmt.order_by(col.desc() if reverse else col.asc())
        stmt = stmt.offset((page - 1) * limit).limit(limit)
        rows = (await self.session.scalars(stmt)).all()
        return [self._to_dict(r) for r in rows], total

    async def get(self, university_id: str) -> dict | None:
        if self.mock_mode or self.session is None:
            for u in MOCK_UNIVERSITIES:
                if u["id"] == university_id:
                    return u
            return None
        row = await self.session.get(University, university_id)
        return self._to_dict(row) if row else None

    async def programs(self, university_id: str) -> list[dict] | None:
        uni = await self.get(university_id)
        if uni is None:
            return None
        return list(uni.get("programs") or [])

    @staticmethod
    def _to_dict(row: University) -> dict:
        return {
            "id": row.id,
            "name": row.name,
            "country": row.country,
            "country_code": row.country_code,
            "state": row.state,
            "city": row.city,
            "website": row.website,
            "domains": row.domains or [],
            "programs": row.programs or [],
        }
