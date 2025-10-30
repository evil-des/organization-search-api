from collections.abc import Sequence

from sqlalchemy import literal, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from models.occupation import Occupation
from repositories.base import BaseRepository


class OccupationRepository(BaseRepository[Occupation]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Occupation, session)

    async def get_descendant_ids(
        self,
        occupation_id: int,
        *,
        max_depth: int | None = None,
        include_self: bool = True,
    ) -> Sequence[int]:
        base_query = (
            select(
                self.model.id.label("id"),
                self.model.parent_id.label("parent_id"),
                literal(0).label("depth"),
            )
            .where(self.model.id == occupation_id)
        )
        descendants_cte = base_query.cte(name="occupation_descendants", recursive=True)

        occupation_alias = aliased(self.model)
        next_depth = descendants_cte.c.depth + 1
        recursive_query = (
            select(
                occupation_alias.id,
                occupation_alias.parent_id,
                next_depth.label("depth"),
            )
            .where(occupation_alias.parent_id == descendants_cte.c.id)
        )
        if max_depth is not None:
            recursive_query = recursive_query.where(next_depth <= max_depth)

        descendants_cte = descendants_cte.union_all(recursive_query)

        stmt = select(descendants_cte.c.id, descendants_cte.c.depth)
        if not include_self:
            stmt = stmt.where(descendants_cte.c.depth > 0)

        result = await self.session.execute(stmt)
        rows = result.all()
        return [row.id for row in rows]
