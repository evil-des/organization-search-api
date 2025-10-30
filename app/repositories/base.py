from collections.abc import Sequence
from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from dependecies.session import SessionDependency
from models.base import DBModel

T = TypeVar('T', bound=DBModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession) -> None:
        self.session = session
        self.model = model

    async def get(self, target_id: int, options: Sequence[ExecutableOption] = None) -> Optional[T]:
        options = options or []
        stmt = select(self.model).options(*options).where(self.model.id == target_id)
        scalar = await self.session.scalars(stmt)
        return scalar.one_or_none()

    async def list(self, *, options: Sequence[ExecutableOption] = None) -> Sequence[T]:
        options = options or []
        stmt = select(self.model).options(*options)
        scalar = await self.session.scalars(stmt)
        return scalar.all()

    async def exists(self, target_id: int) -> bool:
        stmt = select(exists().where(self.model.id == target_id))
        scalar = await self.session.scalars(stmt)
        return scalar.one()

    async def create(self, obj_in: dict[str, Any]) -> T:
        obj = self.model(**obj_in)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: T, obj_in: dict[str, Any]) -> T:
        for key, value in obj_in.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def put(self, target_id: int, obj_in: dict[str, Any]) -> T:
        if not (obj := await self.get(target_id)):
            return await self.create(obj_in)
        return await self.update(obj, obj_in)

    async def delete(self, target_id: int) -> None:
        obj = await self.get(target_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
        return obj

    @classmethod
    def get_repository(cls: Any, session: SessionDependency):
        return cls(session)
