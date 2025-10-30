
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from dependecies.auth import TokenSecurityDependency
from dependecies.organization import OrganizationServiceDependency
from schemas.organization import BuildingResponseSchema

router = APIRouter(
    prefix="/buildings",
    tags=["buildings"],
    dependencies=[TokenSecurityDependency],
)


@router.get(
    "/",
    response_model=list[BuildingResponseSchema],
)
async def list_buildings(
    organization_service: OrganizationServiceDependency,
) -> list[BuildingResponseSchema]:
    return await organization_service.list_buildings()


@router.get(
    "/within-radius",
    response_model=list[BuildingResponseSchema],
)
async def buildings_within_radius(
    organization_service: OrganizationServiceDependency,
    latitude: Annotated[float, Query(ge=-90.0, le=90.0)],
    longitude: Annotated[float, Query(ge=-180.0, le=180.0)],
    radius_meters: Annotated[float, Query(gt=0, alias="radiusMeters")],
) -> list[BuildingResponseSchema]:
    return await organization_service.list_buildings_within_radius(
        latitude=latitude,
        longitude=longitude,
        radius_meters=radius_meters,
    )


@router.get(
    "/within-bounds",
    response_model=list[BuildingResponseSchema],
)
async def buildings_within_bounds(
    organization_service: OrganizationServiceDependency,
    min_latitude: Annotated[float, Query(alias="minLatitude", ge=-90.0, le=90.0)],
    max_latitude: Annotated[float, Query(alias="maxLatitude", ge=-90.0, le=90.0)],
    min_longitude: Annotated[float, Query(alias="minLongitude", ge=-180.0, le=180.0)],
    max_longitude: Annotated[float, Query(alias="maxLongitude", ge=-180.0, le=180.0)],
) -> list[BuildingResponseSchema]:
    if min_latitude > max_latitude:
        raise HTTPException(status_code=400, detail="minLatitude must be <= maxLatitude")
    if min_longitude > max_longitude:
        raise HTTPException(status_code=400, detail="minLongitude must be <= maxLongitude")
    return await organization_service.list_buildings_within_bounds(
        min_latitude=min_latitude,
        max_latitude=max_latitude,
        min_longitude=min_longitude,
        max_longitude=max_longitude,
    )


__all__ = ("router",)
