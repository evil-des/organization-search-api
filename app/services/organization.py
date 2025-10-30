from __future__ import annotations

from collections.abc import Iterable, Sequence
from math import asin, cos, radians, sin, sqrt

from dependecies.repository import (
    BuildingRepositoryDependency,
    OccupationRepositoryDependency,
    OrganizationRepositoryDependency,
)
from models.building import Building
from models.occupation import Occupation
from models.organization import Organization
from models.phone_number import PhoneNumber
from repositories.building import BuildingRepository
from repositories.occupation import OccupationRepository
from repositories.organization import OrganizationRepository
from schemas.organization import (
    BuildingResponseSchema,
    OrganizationAreaResponseSchema,
    OrganizationResponseSchema,
    OccupationResponseSchema,
    PhoneNumberResponseSchema,
)
from services.base import BaseService


class OrganizationService(BaseService):
    MAX_OCCUPATION_DEPTH = 3
    _METERS_PER_DEGREE_LATITUDE = 111_320.0
    _EARTH_RADIUS_METERS = 6_371_000.0

    def __init__(
        self,
        organization_repository: OrganizationRepository,
        building_repository: BuildingRepository,
        occupation_repository: OccupationRepository,
    ) -> None:
        self.organization_repository = organization_repository
        self.building_repository = building_repository
        self.occupation_repository = occupation_repository

    async def get_organization(
        self,
        organization_id: int,
    ) -> OrganizationResponseSchema | None:
        if not (
            organization := await self.organization_repository
            .get_with_details(organization_id)
        ):
            return None
        return self._to_organization_schema(organization)

    async def list_by_building(
        self,
        building_id: int,
    ) -> list[OrganizationResponseSchema]:
        organizations = await (self.organization_repository
                               .list_by_building_id(building_id))
        return self._map_organizations(organizations)

    async def list_by_occupation(
        self,
        occupation_id: int,
    ) -> list[OrganizationResponseSchema]:
        organizations = await (self.organization_repository
                               .list_by_occupation_ids([occupation_id]))
        return self._map_organizations(organizations)

    async def list_by_occupation_tree(
        self,
        occupation_id: int,
        *,
        max_depth: int | None = None,
    ) -> list[OrganizationResponseSchema]:
        depth = self.MAX_OCCUPATION_DEPTH
        if max_depth is not None:
            depth = min(max_depth, self.MAX_OCCUPATION_DEPTH)
        occupation_ids = await self.occupation_repository.get_descendant_ids(
            occupation_id,
            max_depth=depth,
            include_self=True,
        )
        organizations = await (self.organization_repository
                               .list_by_occupation_ids(occupation_ids))
        return self._map_organizations(organizations)

    async def search_by_occupation_hierarchy(
        self,
        occupation_id: int,
    ) -> list[OrganizationResponseSchema]:
        return await self.list_by_occupation_tree(
            occupation_id,
            max_depth=self.MAX_OCCUPATION_DEPTH,
        )

    async def search_by_name(
        self,
        query: str,
        *,
        limit: int | None = None,
    ) -> list[OrganizationResponseSchema]:
        organizations = await (self.organization_repository
                               .search_by_name(query, limit=limit))
        return self._map_organizations(organizations)

    async def list_buildings(self) -> list[BuildingResponseSchema]:
        buildings = await self.building_repository.list_all()
        return self._map_buildings(buildings)

    async def list_buildings_within_radius(
        self,
        *,
        latitude: float,
        longitude: float,
        radius_meters: float,
    ) -> list[BuildingResponseSchema]:
        buildings = await self._fetch_buildings_within_radius(
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius_meters,
        )
        return self._map_buildings(buildings)

    async def list_buildings_within_bounds(
        self,
        *,
        min_latitude: float,
        max_latitude: float,
        min_longitude: float,
        max_longitude: float,
    ) -> list[BuildingResponseSchema]:
        buildings = await self._fetch_buildings_within_bounds(
            min_latitude=min_latitude,
            max_latitude=max_latitude,
            min_longitude=min_longitude,
            max_longitude=max_longitude,
        )
        return self._map_buildings(buildings)

    async def list_organizations_within_radius(
        self,
        *,
        latitude: float,
        longitude: float,
        radius_meters: float,
    ) -> OrganizationAreaResponseSchema:
        buildings = await self._fetch_buildings_within_radius(
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius_meters,
        )
        organizations = await self._fetch_organizations_for_buildings(buildings)
        return OrganizationAreaResponseSchema(
            organizations=self._map_organizations(organizations),
            buildings=self._map_buildings(buildings),
        )

    async def list_organizations_within_bounds(
        self,
        *,
        min_latitude: float,
        max_latitude: float,
        min_longitude: float,
        max_longitude: float,
    ) -> OrganizationAreaResponseSchema:
        buildings = await self._fetch_buildings_within_bounds(
            min_latitude=min_latitude,
            max_latitude=max_latitude,
            min_longitude=min_longitude,
            max_longitude=max_longitude,
        )
        organizations = await self._fetch_organizations_for_buildings(buildings)
        return OrganizationAreaResponseSchema(
            organizations=self._map_organizations(organizations),
            buildings=self._map_buildings(buildings),
        )

    async def _fetch_buildings_within_radius(
        self,
        *,
        latitude: float,
        longitude: float,
        radius_meters: float,
    ) -> list[Building]:
        bounds = self._get_bounding_box(latitude, longitude, radius_meters)
        buildings = await self.building_repository.list_within_bounds(**bounds)
        return [
            building
            for building in buildings
            if self._distance_between(
                latitude,
                longitude,
                building.latitude,
                building.longitude,
            )
            <= radius_meters
        ]

    async def _fetch_buildings_within_bounds(
        self,
        *,
        min_latitude: float,
        max_latitude: float,
        min_longitude: float,
        max_longitude: float,
    ) -> list[Building]:
        buildings = await self.building_repository.list_within_bounds(
            min_latitude=min_latitude,
            max_latitude=max_latitude,
            min_longitude=min_longitude,
            max_longitude=max_longitude,
        )
        return list(buildings)

    async def _fetch_organizations_for_buildings(
        self,
        buildings: Iterable[Building],
    ) -> Sequence[Organization]:
        building_ids = {building.id for building in buildings}
        if not building_ids:
            return []
        return await self.organization_repository.list_by_building_ids(building_ids)

    def _map_buildings(
        self,
        buildings: Iterable[Building],
    ) -> list[BuildingResponseSchema]:
        return [self._to_building_schema(building) for building in buildings]

    def _map_organizations(
        self,
        organizations: Iterable[Organization],
    ) -> list[OrganizationResponseSchema]:
        return [
            self._to_organization_schema(organization)
            for organization in organizations
        ]

    def _to_building_schema(self, building: Building) -> BuildingResponseSchema:
        return BuildingResponseSchema(
            id=building.id,
            address=building.address,
            latitude=building.latitude,
            longitude=building.longitude,
            organization_id=building.organization_id,
        )

    def _to_occupation_schema(self, occupation: Occupation) -> OccupationResponseSchema:
        return OccupationResponseSchema(
            id=occupation.id,
            name=occupation.name,
            parent_id=occupation.parent_id,
        )

    def _to_phone_schema(self, phone: PhoneNumber) -> PhoneNumberResponseSchema:
        return PhoneNumberResponseSchema(
            id=phone.id,
            value=phone.value,
            is_primary=phone.is_primary,
            type=phone.type,
            comment=phone.comment,
        )

    def _to_organization_schema(self, organization: Organization) -> OrganizationResponseSchema:
        building = organization.building
        occupations = sorted(
            organization.occupations,
            key=lambda item: (item.parent_id or 0, item.id),
        )
        phones = sorted(
            organization.phones,
            key=lambda item: (not item.is_primary, item.id),
        )
        return OrganizationResponseSchema(
            id=organization.id,
            name=organization.name,
            building=self._to_building_schema(building) if building else None,
            occupations=[self._to_occupation_schema(occupation) for occupation in occupations],
            phones=[self._to_phone_schema(phone) for phone in phones],
        )

    def _get_bounding_box(
        self,
        latitude: float,
        longitude: float,
        radius_meters: float,
    ) -> dict[str, float]:
        lat_delta = radius_meters / self._METERS_PER_DEGREE_LATITUDE
        lon_denominator = max(cos(radians(latitude)), 1e-6)
        lon_delta = radius_meters / (self._METERS_PER_DEGREE_LATITUDE * lon_denominator)
        return {
            "min_latitude": max(latitude - lat_delta, -90.0),
            "max_latitude": min(latitude + lat_delta, 90.0),
            "min_longitude": max(longitude - lon_delta, -180.0),
            "max_longitude": min(longitude + lon_delta, 180.0),
        }

    def _distance_between(
        self,
        lat_a: float,
        lon_a: float,
        lat_b: float,
        lon_b: float,
    ) -> float:
        lat_a_rad = radians(lat_a)
        lat_b_rad = radians(lat_b)
        delta_lat = radians(lat_b - lat_a)
        delta_lon = radians(lon_b - lon_a)

        a = (
            sin(delta_lat / 2) ** 2
            + cos(lat_a_rad) * cos(lat_b_rad) * sin(delta_lon / 2) ** 2
        )
        c = 2 * asin(min(1.0, sqrt(a)))
        return self._EARTH_RADIUS_METERS * c

    @classmethod
    def get_service(
        cls,
        organization_repository: OrganizationRepositoryDependency,
        building_repository: BuildingRepositoryDependency,
        occupation_repository: OccupationRepositoryDependency,
    ) -> "OrganizationService":
        return cls(
            organization_repository=organization_repository,
            building_repository=building_repository,
            occupation_repository=occupation_repository,
        )
