from enum import Enum, IntEnum


class StrEnum(str, Enum):
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class EnvEnum(StrEnum):
    DEV: str = "dev"
    STAGGING: str = "stagging"
    PROD: str = "prod"


class ImageSizeEnum(IntEnum):
    SIZE_32: int = 32
    SIZE_64: int = 64
    SIZE_128: int = 128
    SIZE_256: int = 256
