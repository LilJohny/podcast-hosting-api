import datetime
import enum
import uuid as uuid_lib

from pydantic import AnyUrl, FileUrl
from sqlmodel import SQLModel, Field, Enum, Column
from models import DeletableModel, UUIDModel


class Language(str, enum.Enum):
    english = "en"


class Category(str, enum.Enum):
    arts_books = "Arts/Books"


class ImageBase(SQLModel):
    file_url: FileUrl
    title: str


class ShowBase(SQLModel):
    title: str
    show_link: AnyUrl
    media_link: AnyUrl
    description: str
    generator: str
    language: Language = Field(sa_column=Column(Enum(Language)))
    show_copyright: str
    last_build_date: datetime.datetime
    image: ImageBase
    podcast_owner: str
    is_locked: bool
    category: Category = Field(sa_column=Column(Enum(Category)))


class Image(ImageBase, UUIDModel, DeletableModel, table=True):
    pass


class Show(ShowBase, UUIDModel, DeletableModel, table=True):
    image: uuid_lib.UUID = Field(default=None, foreign_key="image.id")
