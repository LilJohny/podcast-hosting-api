from pydantic import FileUrl
from sqlmodel import SQLModel

from models import UUIDModel, DeletableModel


class ImageBase(SQLModel):
    file_url: FileUrl
    title: str


class Image(ImageBase, UUIDModel, DeletableModel, table=True):
    pass

