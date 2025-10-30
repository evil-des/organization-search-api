from collections.abc import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.sql import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.building import Building
from models.occupation import Occupation
from models.organization import Organization
from repositories.base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Organization, session)

    def _base_select(self) -> Select[tuple[Organization]]:
        return (
            select(self.model)
            .options(
                selectinload(self.model.building),
                selectinload(self.model.occupations),
                selectinload(self.model.phones),
            )
        )

    async def list_by_building_id(self, building_id: int) -> Sequence[Organization]:
        stmt = (
            self._base_select()
            .join(self.model.building)
            .where(Building.id == building_id)
        )
        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def list_by_building_ids(self, building_ids: Iterable[int]) -> Sequence[Organization]:
        building_ids = list(set(building_ids))
        if not building_ids:
            return []
        stmt = (
            self._base_select()
            .join(self.model.building)
            .where(Building.id.in_(building_ids))
        )
        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def list_by_occupation_ids(self, occupation_ids: Iterable[int]) -> Sequence[Organization]:
        occupation_ids = list(set(occupation_ids))
        if not occupation_ids:
            return []
        stmt = (
            self._base_select()
            .join(self.model.occupations)
            .where(Occupation.id.in_(occupation_ids))
            .distinct()
        )
        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def search_by_name(self, query: str, *, limit: int | None = None) -> Sequence[Organization]:
        pattern = f"%{query.strip()}%"
        stmt = (
            self._base_select()
            .where(self.model.name.ilike(pattern))
            .order_by(self.model.name.asc())
        )
        if limit:
            stmt = stmt.limit(limit)
        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def get_with_details(self, organization_id: int) -> Organization | None:
        stmt = self._base_select().where(self.model.id == organization_id)
        result = await self.session.scalars(stmt)
        return result.unique().one_or_none()
