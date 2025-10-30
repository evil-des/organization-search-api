from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from dependecies.auth import TokenSecurityDependency
from dependecies.organization import OrganizationServiceDependency
from schemas.organization import (
    OrganizationAreaResponseSchema,
    OrganizationResponseSchema,
)

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[TokenSecurityDependency],
)


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponseSchema,
)
async def get_organization(
    organization_id: int,
    organization_service: OrganizationServiceDependency,
) -> OrganizationResponseSchema:
    if organization := await organization_service.get_organization(organization_id):
        return organization
    raise HTTPException(status_code=404, detail="Organization not found")


@router.get(
    "/by-building/{building_id}",
    response_model=list[OrganizationResponseSchema],
)
async def list_by_building(
    building_id: int,
    organization_service: OrganizationServiceDependency,
) -> list[OrganizationResponseSchema]:
    return await organization_service.list_by_building(building_id)


@router.get(
    "/by-occupation/{occupation_id}",
    response_model=list[OrganizationResponseSchema],
)
async def list_by_occupation(
    occupation_id: int,
    organization_service: OrganizationServiceDependency,
    include_children: Annotated[bool, Query(alias="includeChildren")] = True,
    max_depth: Annotated[int | None, Query(alias="maxDepth", ge=1, le=10)] = None,
) -> list[OrganizationResponseSchema]:
    if include_children:
        return await organization_service.list_by_occupation_tree(
            occupation_id,
            max_depth=max_depth,
        )
    return await organization_service.list_by_occupation(occupation_id)


@router.get(
    "/search/by-name",
    response_model=list[OrganizationResponseSchema],
)
async def search_by_name(
    organization_service: OrganizationServiceDependency,
    query: Annotated[str, Query(min_length=1, alias="q")],
    limit: Annotated[int | None, Query(ge=1, le=100)] = None,
) -> list[OrganizationResponseSchema]:
    return await organization_service.search_by_name(query, limit=limit)


@router.get(
    "/search/within-radius",
    response_model=OrganizationAreaResponseSchema,
)
async def organizations_within_radius(
    organization_service: OrganizationServiceDependency,
    latitude: Annotated[float, Query(ge=-90.0, le=90.0)],
    longitude: Annotated[float, Query(ge=-180.0, le=180.0)],
    radius_meters: Annotated[float, Query(gt=0, alias="radiusMeters")],
) -> OrganizationAreaResponseSchema:
    return await organization_service.list_organizations_within_radius(
        latitude=latitude,
        longitude=longitude,
        radius_meters=radius_meters,
    )


@router.get(
    "/search/within-bounds",
    response_model=OrganizationAreaResponseSchema,
)
async def organizations_within_bounds(
    organization_service: OrganizationServiceDependency,
    min_latitude: Annotated[float, Query(alias="minLatitude", ge=-90.0, le=90.0)],
    max_latitude: Annotated[float, Query(alias="maxLatitude", ge=-90.0, le=90.0)],
    min_longitude: Annotated[float, Query(alias="minLongitude", ge=-180.0, le=180.0)],
    max_longitude: Annotated[float, Query(alias="maxLongitude", ge=-180.0, le=180.0)],
) -> OrganizationAreaResponseSchema:
    if min_latitude > max_latitude:
        raise HTTPException(status_code=400, detail="minLatitude must be <= maxLatitude")
    if min_longitude > max_longitude:
        raise HTTPException(status_code=400, detail="minLongitude must be <= maxLongitude")
    return await organization_service.list_organizations_within_bounds(
        min_latitude=min_latitude,
        max_latitude=max_latitude,
        min_longitude=min_longitude,
        max_longitude=max_longitude,
    )
