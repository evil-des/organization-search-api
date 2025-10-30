import asyncio
from typing import Iterable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import Session
from enums.phone_number import PhoneNumberType
from models.building import Building
from models.occupation import Occupation
from models.organization import Organization
from models.phone_number import PhoneNumber


async def database_has_data(session: AsyncSession) -> bool:
    result = await session.execute(
        select(func.count()).select_from(Organization)
    )
    return result.scalar_one() > 0


async def seed_occupations(session: AsyncSession) -> dict[str, Occupation]:
    hierarchy = [
        {
            "name": "Еда",
            "children": [
                {"name": "Кофейни"},
                {"name": "Рестораны"},
                {"name": "Пекарни"},
            ],
        },
        {
            "name": "Здоровье",
            "children": [
                {"name": "Аптеки"},
                {"name": "Клиники"},
            ],
        },
        {
            "name": "Развлечения",
            "children": [
                {"name": "Кинотеатры"},
                {"name": "Музеи"},
            ],
        },
    ]

    occupations: dict[str, Occupation] = {}

    async def create_node(node: dict, parent: Occupation | None = None) -> None:
        occupation = Occupation(name=node["name"], parent=parent)
        session.add(occupation)
        await session.flush()
        occupations[occupation.name] = occupation

        for child in node.get("children", []):
            await create_node(child, occupation)

    for item in hierarchy:
        await create_node(item)

    return occupations


async def seed_organizations(
    session: AsyncSession,
    occupations: dict[str, Occupation],
) -> None:
    organizations = [
        {
            "name": "Кофемания Арбат",
            "occupations": ["Кофейни"],
            "building": {
                "address": "г. Москва, ул. Арбат, 18",
                "latitude": 55.749709,
                "longitude": 37.595149,
            },
            "phones": [
                {
                    "value": "+74951234567",
                    "is_primary": True,
                    "type": PhoneNumberType.WORK,
                },
                {
                    "value": "+79261234567",
                    "is_primary": False,
                    "type": PhoneNumberType.MOBILE,
                    "comment": "Доставка",
                },
            ],
        },
        {
            "name": "Чайхана Пахлава",
            "occupations": ["Рестораны"],
            "building": {
                "address": "г. Москва, пр-т Мира, 26, стр. 1",
                "latitude": 55.781164,
                "longitude": 37.633091,
            },
            "phones": [
                {
                    "value": "+74956667788",
                    "is_primary": True,
                    "type": PhoneNumberType.WORK,
                },
            ],
        },
        {
            "name": "Городская клиника №1",
            "occupations": ["Клиники"],
            "building": {
                "address": "г. Санкт-Петербург, Невский пр., 44",
                "latitude": 59.932087,
                "longitude": 30.347661,
            },
            "phones": [
                {
                    "value": "+78124445566",
                    "is_primary": True,
                    "type": PhoneNumberType.WORK,
                },
            ],
        },
        {
            "name": "Аптека 36,6",
            "occupations": ["Аптеки"],
            "building": {
                "address": "г. Казань, ул. Баумана, 54",
                "latitude": 55.794207,
                "longitude": 49.107722,
            },
            "phones": [
                {
                    "value": "+78432998877",
                    "is_primary": True,
                    "type": PhoneNumberType.WORK,
                },
            ],
        },
        {
            "name": "Кулинария Хлеб да Соль",
            "occupations": ["Пекарни"],
            "building": {
                "address": "г. Нижний Новгород, ул. Большая Покровская, 21",
                "latitude": 56.326797,
                "longitude": 44.005986,
            },
            "phones": [
                {
                    "value": "+78312001122",
                    "is_primary": True,
                    "type": PhoneNumberType.WORK,
                },
            ],
        },
    ]

    def phone_factory(
        organization: Organization, phones: Iterable[dict]
    ) -> list[PhoneNumber]:
        return [
            PhoneNumber(
                organization=organization,
                value=phone["value"],
                is_primary=phone.get("is_primary", False),
                type=phone.get("type", PhoneNumberType.WORK),
                comment=phone.get("comment"),
            )
            for phone in phones
        ]

    for data in organizations:
        org = Organization(name=data["name"])
        org.occupations = [
            occupations[name]
            for name in data["occupations"]
            if name in occupations
        ]
        session.add(org)
        await session.flush()

        building_data = data["building"]
        building = Building(
            address=building_data["address"],
            latitude=building_data["latitude"],
            longitude=building_data["longitude"],
            organization=org,
        )
        session.add(building)

        for phone in phone_factory(org, data["phones"]):
            session.add(phone)


async def seed() -> None:
    async with Session() as session:
        if await database_has_data(session):
            return

        occupations = await seed_occupations(session)
        await seed_organizations(session, occupations)
        await session.commit()


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()
