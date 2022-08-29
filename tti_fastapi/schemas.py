from typing import Dict, Union

from pydantic import BaseModel, Field, HttpUrl

from enums import ResponseStatusEnum


class ImageGenerationRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="try adding increments to your prompt such as 'oil on canvas', 'a painting', 'a book cover'",
    )
    steps: int = Field(
        default=45, ge=1, le=50, description="more steps can increase quality but will take longer to generate"
    )
    seed: int = Field(default=1, ge=0, le=2147483647)
    width: int = Field(default=512, ge=32, le=512)
    height: int = Field(default=512, ge=32, le=512)
    images: int = Field(2, ge=1, le=4, description="How many images you wish to generate")
    guidance_scale: float = Field(7.5, ge=0, le=50, description="how much the prompt will influence the results")


class AsyncTaskResponse(BaseModel):
    task_id: str


class Error(BaseModel):
    status_code: int
    error_message: str


class ImageGenerationResponse(BaseModel):
    status: ResponseStatusEnum = ResponseStatusEnum.PENDING
    updated_at: float = 0.0
    result: Union[Dict[str, HttpUrl], None] = None
