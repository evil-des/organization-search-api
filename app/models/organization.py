from typing import Optional, TYPE_CHECKING
from sqlalchemy import (BigInteger, event, ForeignKey, String,
                        CheckConstraint, UniqueConstraint, Table)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import DBModel
from models.mixins import CreatedAtMixin
from models.assoc import organization_occupations

if TYPE_CHECKING:
    from models.occupation import Occupation
    from models.phone_number import PhoneNumber
    from models.building import Building


class Organization(DBModel, CreatedAtMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(200), unique=True)
    occupations: Mapped[list["Occupation"]] = relationship(
        "Occupation",
        secondary=organization_occupations,
        back_populates="organizations",
        lazy="selectin",
    )
    phones: Mapped[list["PhoneNumber"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    building: Mapped[Optional["Building"]] = relationship(
        back_populates="organization",
        uselist=False,
    )
