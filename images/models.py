from sqladmin import ModelAdmin
from sqlmodel import SQLModel

from models import UUIDModel, DeletableModel


class ImageParam(SQLModel):
    title: str


class ImageResponse(ImageParam, UUIDModel):
    file_url: str


class Image(ImageResponse, DeletableModel, table=True):
    pass


class ImageAdmin(ModelAdmin, model=Image):
    column_list = [Image.id, Image.title, Image.file_url, Image.is_removed]
