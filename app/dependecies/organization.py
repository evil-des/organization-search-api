from typing import Annotated

from fastapi import Depends

from services.organization import OrganizationService

OrganizationServiceDependency = Annotated[
    OrganizationService,
    Depends(OrganizationService.get_service),
]
