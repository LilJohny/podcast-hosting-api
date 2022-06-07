from pydantic import BaseModel

from schemas import UUIDSchema


class ImageCreate(BaseModel):
    title: str


class ImageResponse(ImageCreate, UUIDSchema):
    file_url: str
