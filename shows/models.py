import datetime
import enum
import uuid
import uuid as uuid_lib
from typing import Set

from pydantic import AnyUrl
from sqlmodel import SQLModel, Field, Enum, Column, String, ARRAY

from models import DeletableModel, UUIDModel
from users.db_adapter import UserTable


class Language(str, enum.Enum):
    english = "en"


class Category(str, enum.Enum):
    arts_books = "Arts/Books"


class ShowCreate(SQLModel):
    title: str
    description: str
    generator: str
    language: Language = Field(sa_column=Column(Enum(Language)))
    show_copyright: str
    last_build_date: datetime.datetime
    owner: uuid.UUID = Field(default=None, foreign_key=UserTable.id)
    is_locked: bool
    category: Category = Field(sa_column=Column(Enum(Category)))
    series: Set[str] = Field(default=None, sa_column=Column(ARRAY(String())))
    featured: bool = Field(default=False)


class ShowParam(ShowCreate):
    show_link: str
    media_link: str


class ShowResponse(ShowParam, UUIDModel):
    image: uuid_lib.UUID = Field(default=None, foreign_key="image.id")


class Show(ShowResponse, DeletableModel, table=True):
    feed_file_link: str
