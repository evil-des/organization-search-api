from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import DBModel
from models.mixins import CreatedAtMixin

if TYPE_CHECKING:
    from models.user import User


class Building(DBModel, CreatedAtMixin):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(200), nullable=False)

    latitude:  Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    organization: Mapped["Organization"] = relationship(back_populates="building")

    __table_args__ = (
        CheckConstraint("latitude  >= -90  AND latitude  <= 90",  name="ck_lat_range"),
        CheckConstraint("longitude >= -180 AND longitude <= 180", name="ck_lon_range"),
    )
