import datetime
import enum
import uuid as uuid_lib
from typing import List

from pydantic import AnyUrl
from sqlmodel import SQLModel, Field, Enum, Column

from images.models import ImageParam
from models import DeletableModel, UUIDModel


class Language(str, enum.Enum):
    english = "en"


class Category(str, enum.Enum):
    arts_books = "Arts/Books"


class ShowParam(SQLModel):
    title: str
    show_link: AnyUrl
    media_link: AnyUrl
    description: str
    generator: str
    language: Language = Field(sa_column=Column(Enum(Language)))
    show_copyright: str
    last_build_date: datetime.datetime
    image: ImageParam
    podcast_owner: str
    is_locked: bool
    category: Category = Field(sa_column=Column(Enum(Category)))
    series: List[str]


class ShowResponse(ShowParam, UUIDModel):
    image: uuid_lib.UUID = Field(default=None, foreign_key="image.id")


class Show(ShowResponse, DeletableModel, table=True):
    pass
