from sqlalchemy import Column, ForeignKey, UniqueConstraint, Table
from models.base import DBModel


organization_occupations = Table(
    "organization_occupations",
    DBModel.metadata,
    Column(
        "org_id",
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "occupation_id",
        ForeignKey("occupations.id", ondelete="RESTRICT"),
        primary_key=True,
    ),
    UniqueConstraint("org_id", "occupation_id", name="uq_org_occ"),
)
