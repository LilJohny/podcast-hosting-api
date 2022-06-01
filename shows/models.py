import datetime
import enum
import uuid
import uuid as uuid_lib
from typing import Set

from sqladmin import ModelAdmin
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
    language: Language = Field(sa_column=Column(Enum(Language)))
    show_copyright: str
    category: Category = Field(sa_column=Column(Enum(Category)))
    series: Set[str] = Field(default=None, sa_column=Column(ARRAY(String())))


class ShowParam(ShowCreate):
    show_link: str
    media_link: str


class ShowResponse(ShowParam, UUIDModel):
    generator: str
    featured: bool = Field(default=False)
    image: uuid_lib.UUID = Field(default=None, foreign_key="image.id")
    is_locked: bool = Field(default=True)
    owner: uuid.UUID = Field(default=None, foreign_key=UserTable.id)
    last_build_date: datetime.datetime
    feed_file_link: str


class Show(ShowResponse, DeletableModel, table=True):
    pass


class ShowAdmin(ModelAdmin, model=Show):
    column_list = [Show.language,
                   Show.category,
                   Show.series,
                   Show.is_removed,
                   Show.id,
                   Show.title,
                   Show.description,
                   Show.show_copyright,
                   Show.show_link,
                   Show.media_link,
                   Show.generator,
                   Show.featured,
                   Show.image,
                   Show.is_locked,
                   Show.owner,
                   Show.last_build_date,
                   Show.feed_file_link]
