from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint, CheckConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import DBModel
from models.mixins import CreatedAtMixin, UpdatedAtMixin
from enums.phone_number import PhoneNumberType

if TYPE_CHECKING:
    from models.organization import Organization


class PhoneNumber(DBModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "phone_numbers"

    value: Mapped[str] = mapped_column(String(16), nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean(), default=False)

    type: Mapped[PhoneNumberType] = mapped_column(
        default=PhoneNumberType.WORK,
        server_default=str(PhoneNumberType.WORK),
    )
    comment: Mapped[str | None] = mapped_column(String(200))

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    organization: Mapped["Organization"] = relationship(back_populates="phones")

    __table_args__ = (
        UniqueConstraint("organization_id", "value", name="uq_org_phone"),
        CheckConstraint(r"value ~ '^\+[0-9]{1,15}$'", name="ck_phone_e164_format"),
    )
