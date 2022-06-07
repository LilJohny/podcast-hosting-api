import uuid

from sqladmin import ModelAdmin
from sqlalchemy import Column, BOOLEAN, String
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import SQLModel

from models import UUIDModel, DeletableModel
from settings import Base


class ImageParam(SQLModel):
    title: str


class ImageResponse(ImageParam, UUIDModel):
    file_url: str


# class Image(ImageResponse, DeletableModel, table=True):
#     pass


