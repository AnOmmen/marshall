from enum import Enum, auto


class AccessLevel(Enum):
    ADMIN = auto()
    MEMBER = auto()
    GUEST = auto()
