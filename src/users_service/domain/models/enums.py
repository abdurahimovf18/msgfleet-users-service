from enum import Enum


class STREnum(str, Enum): pass


class UserLanguages(STREnum):
    """Supported user languages."""
    EN = "EN"
    UZ = "UZ"
    RU = "RU"
