from pydantic import HttpUrl
from sqlmodel import SQLModel

from models import UUIDModel, DeletableModel


class ImageDTO(SQLModel):
    file_url: str
    title: str


class Image(ImageDTO, UUIDModel, DeletableModel, table=True):
    pass
