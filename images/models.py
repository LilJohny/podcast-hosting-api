from pydantic import  HttpUrl
from sqlmodel import SQLModel

from models import UUIDModel, DeletableModel


class ImageBase(SQLModel):
    file_url: HttpUrl
    title: str


class Image(ImageBase, UUIDModel, DeletableModel, table=True):
    pass

