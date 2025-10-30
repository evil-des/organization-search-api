from sqlalchemy.ext.asyncio import AsyncSession

from models.phone_number import PhoneNumber
from repositories.base import BaseRepository


class PhoneNumberRepository(BaseRepository[PhoneNumber]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(PhoneNumber, session)
