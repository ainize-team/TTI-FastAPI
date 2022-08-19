from pydantic import BaseModel, Field

from enums import ImageSizeEnum


class GenerationRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="try adding increments to your prompt such as 'oil on canvas', 'a painting', 'a book cover'",
    )
    steps: int = Field(45, ge=1, le=50, description="more steps can increase quality but will take longer to generate")
    width: ImageSizeEnum = ImageSizeEnum.SIZE_256
    height: ImageSizeEnum = ImageSizeEnum.SIZE_256
    images: int = Field(2, ge=1, le=4, description="How many images you wish to generate")
    diversity_scale: float = Field(
        5, ge=1, le=15, description="How different from one another you wish the images to be"
    )
