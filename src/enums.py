from enum import Enum


class StrEnum(str, Enum):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class EnvEnum(StrEnum):
    DEV: str = "dev"
    PROD: str = "prod"


class ResponseStatusEnum(StrEnum):
    PENDING: str = "pending"
    ASSIGNED: str = "assigned"
    COMPLETED: str = "completed"
    ERROR: str = "error"


class ModelEnum(StrEnum):
    STABLE_DIFFUSION_V1_4 = "stable-diffusion-v1-4"
    STABLE_DIFFUSION_V1_5 = "stable-diffusion-v1-5"
    STABLE_DIFFUSION_V2 = "stable-diffusion-v2"
    STABLE_DIFFUSION_V2_1 = "stable-diffusion-v2-1"
