from sqlmodel import SQLModel

from models import UUIDModel, DeletableModel


class ImageParam(SQLModel):
    title: str


class Image(ImageParam, UUIDModel, DeletableModel, table=True):
    file_url: str


class ImageResponse(ImageParam, UUIDModel):
    file_url: str
