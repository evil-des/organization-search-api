from typing import Optional

from enums.phone_number import PhoneNumberType
from schemas.base import ResponseModel


class BuildingResponseSchema(ResponseModel):
    id: int
    address: str
    latitude: float
    longitude: float
    organization_id: int


class OccupationResponseSchema(ResponseModel):
    id: int
    name: str
    parent_id: Optional[int]


class PhoneNumberResponseSchema(ResponseModel):
    id: int
    value: str
    is_primary: bool
    type: PhoneNumberType
    comment: Optional[str]


class OrganizationResponseSchema(ResponseModel):
    id: int
    name: str
    building: Optional[BuildingResponseSchema]
    occupations: list[OccupationResponseSchema]
    phones: list[PhoneNumberResponseSchema]


class OrganizationAreaResponseSchema(ResponseModel):
    organizations: list[OrganizationResponseSchema]
    buildings: list[BuildingResponseSchema]
