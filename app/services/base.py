from abc import ABC, abstractmethod
from typing import Self, TypeVar

from repositories.base import BaseRepository

R = TypeVar('R', bound=BaseRepository)


class BaseService(ABC):
    @classmethod
    @abstractmethod
    def get_service(cls, *args, **kwargs) -> Self:
        pass
