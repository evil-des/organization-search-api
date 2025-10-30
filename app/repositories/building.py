from collections.abc import Iterable, Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.building import Building
from repositories.base import BaseRepository


class BuildingRepository(BaseRepository[Building]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Building, session)

    async def list_all(self) -> Sequence[Building]:
        stmt = select(self.model).options(selectinload(self.model.organization))
        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def list_by_ids(self, ids: Iterable[int]) -> Sequence[Building]:
        ids = list(set(ids))
        if not ids:
            return []
        stmt = (
            select(self.model)
            .where(self.model.id.in_(ids))
            .options(selectinload(self.model.organization))
        )
        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def list_within_bounds(
        self,
        *,
        min_latitude: float,
        max_latitude: float,
        min_longitude: float,
        max_longitude: float,
    ) -> Sequence[Building]:
        stmt = (
            select(self.model)
            .where(
                and_(
                    self.model.latitude >= min_latitude,
                    self.model.latitude <= max_latitude,
                    self.model.longitude >= min_longitude,
                    self.model.longitude <= max_longitude,
                )
            )
            .options(selectinload(self.model.organization))
        )
        result = await self.session.scalars(stmt)
        return result.unique().all()
