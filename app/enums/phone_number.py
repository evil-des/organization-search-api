from enum import auto
from enums.base import SameCaseStrEnum


class PhoneNumberType(SameCaseStrEnum):
    WORK = auto()
    MOBILE = auto()
    FAX = auto()
