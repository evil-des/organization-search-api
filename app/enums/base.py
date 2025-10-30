from enum import StrEnum


class SameCaseStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Return the same-cased version of the member name.
        """
        return name
