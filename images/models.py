from sqladmin import ModelAdmin
from sqlmodel import SQLModel

from models import UUIDModel, DeletableModel


class ImageParam(SQLModel):
    title: str


class ImageResponse(ImageParam, UUIDModel):
    file_url: str


class Image(ImageResponse, DeletableModel, table=True):
    pass
