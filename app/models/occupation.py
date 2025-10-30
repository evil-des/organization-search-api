from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import DBModel
from models.mixins import CreatedAtMixin
from models.assoc import organization_occupations

if TYPE_CHECKING:
    from models.organization import Organization


class Occupation(DBModel, CreatedAtMixin):
    __tablename__ = "occupations"
    name: Mapped[str] = mapped_column(String(200))

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("occupations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    parent: Mapped[Optional["Occupation"]] = relationship(
        back_populates="children",
        remote_side="Occupation.id",
    )
    children: Mapped[list["Occupation"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    organizations: Mapped[list["Organization"]] = relationship(
        back_populates="occupations",
        secondary=organization_occupations,
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint("parent_id", "name", name="uq_occupations_parent_name"),
        CheckConstraint(
            "parent_id IS NULL OR parent_id != id",
            name="ck_occupations_no_self_parent"
        ),
    )
