from typing import Annotated
from fastapi import Depends
from repositories import (
    BuildingRepository,
    OccupationRepository,
    OrganizationRepository,
    PhoneNumberRepository,
)

BuildingRepositoryDependency = Annotated[
    BuildingRepository,
    Depends(BuildingRepository.get_repository),
]
OccupationRepositoryDependency = Annotated[
    OccupationRepository,
    Depends(OccupationRepository.get_repository),
]
OrganizationRepositoryDependency = Annotated[
    OrganizationRepository,
    Depends(OrganizationRepository.get_repository),
]
PhoneNumberRepositoryDependency = Annotated[
    PhoneNumberRepository,
    Depends(PhoneNumberRepository.get_repository),
]
