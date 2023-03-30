from typing import Dict, Optional, Union

from pydantic import BaseModel, Field, HttpUrl, validator

from enums import ModelEnum, ResponseStatusEnum, SchedulerType


class ImageGenerationDiscordParams(BaseModel):
    user_id: str = Field(..., description="The user's unique ID.")
    guild_id: str = Field(..., description="The guild's ID.")
    channel_id: str = Field(..., description="The channel ID.")
    message_id: str = Field(..., description="The message ID.")


class ImageGenerationParams(BaseModel):
    prompt: str = Field(
        ...,
        description="try adding increments to your prompt such as 'oil on canvas', 'a painting', 'a book cover'",
    )
    negative_prompt: Optional[str] = Field(
        "",
        description="prompt value that you do not want to see in the resulting image",
    )
    steps: int = Field(
        default=30, ge=10, le=150, description="more steps can increase quality but will take longer to generate"
    )
    seed: int = Field(default=1, ge=0, le=4294967295)
    width: int = Field(default=768, ge=512, le=1024)
    height: int = Field(default=768, ge=512, le=1024)
    images: int = Field(2, ge=1, le=4, description="How many images you wish to generate")
    guidance_scale: float = Field(7, ge=0, le=20, description="how much the prompt will influence the results")
    model_id: ModelEnum = Field(ModelEnum.STABLE_DIFFUSION_V2_1_768, description="diffusion model id")
    scheduler_type: SchedulerType = Field(SchedulerType.DDIM, description="Scheduler Type")

    @validator("width")
    def validate_width(cls, v):
        if v % 64 != 0:
            raise ValueError("ensure that value is a multiple of 64")
        return v

    @validator("height")
    def validate_height(cls, v):
        if v % 64 != 0:
            raise ValueError("ensure that value is a multiple of 64")
        return v


class ImageGenerationRequest(BaseModel):
    discord: ImageGenerationDiscordParams
    params: ImageGenerationParams


class AsyncTaskResponse(BaseModel):
    task_id: str
    updated_at: int = 0


class Error(BaseModel):
    status_code: int
    error_message: str


class ImageGenerationResult(BaseModel):
    url: HttpUrl
    origin_url: Optional[HttpUrl]
    is_filtered: Optional[bool]


class ImageGenerationResponse(BaseModel):
    status: ResponseStatusEnum = ResponseStatusEnum.PENDING
    updated_at: int = 0
    result: Union[Dict[str, ImageGenerationResult], None, str] = None


class ImageGenerationTxHashResponse(BaseModel):
    status: ResponseStatusEnum = ResponseStatusEnum.PENDING
    result: Dict[ResponseStatusEnum, str]
    updated_at: int = 0
