"""University service layer."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.core.responses import clamp_pagination
from app.modules.universities.repository import UniversityRepository
from app.modules.universities.schemas import ProgramOut, UniversityOut


class UniversityService:
    def __init__(self, session: AsyncSession | None, mock_mode: bool):
        self.repo = UniversityRepository(session, mock_mode)

    async def list_universities(
        self,
        *,
        page: int = 1,
        limit: int = 20,
        country: str | None = None,
        name: str | None = None,
        q: str | None = None,
        sort: str = "name",
    ) -> tuple[list[UniversityOut], int, int, int]:
        page, limit = clamp_pagination(page, limit)
        rows, total = await self.repo.list(
            page=page, limit=limit, country=country, name=name, q=q, sort=sort
        )
        data = [UniversityOut.model_validate(self._public(r)) for r in rows]
        return data, total, page, limit

    async def get_university(self, university_id: str) -> UniversityOut:
        row = await self.repo.get(university_id)
        if not row:
            raise NotFoundError(f"University '{university_id}' not found")
        return UniversityOut.model_validate(self._public(row))

    async def get_programs(self, university_id: str) -> list[ProgramOut]:
        programs = await self.repo.programs(university_id)
        if programs is None:
            raise NotFoundError(f"University '{university_id}' not found")
        return [ProgramOut.model_validate(p) for p in programs]

    @staticmethod
    def _public(row: dict) -> dict:
        return {k: v for k, v in row.items() if k != "programs"}
