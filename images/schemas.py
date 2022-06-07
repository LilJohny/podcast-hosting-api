from pydantic import BaseModel

from schemas import UUIDModel


class ImageCreate(BaseModel):
    title: str


class ImageResponse(ImageCreate, UUIDModel):
    file_url: str
