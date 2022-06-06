import datetime
import enum
import uuid
import uuid as uuid_lib
from typing import Set, List, Optional
from sqladmin import ModelAdmin
from sqlmodel import SQLModel, Field, Enum, Column
from models import DeletableModel, UUIDModel
from users.db import User


class Language(str, enum.Enum):
    english = "en"


class Category(str, enum.Enum):
    arts_books = "Arts/Books"


class BaseShow(SQLModel):
    title: str
    description: str
    language: Language = Field(sa_column=Column(Enum(Language)))
    show_copyright: str
    category: Category = Field(sa_column=Column(Enum(Category)))


class ShowCreate(BaseShow):
    series: Set[str]


class ShowUpdate(ShowCreate):
    pass


class Show(BaseShow, UUIDModel, DeletableModel, table=True):
    show_link: str
    media_link: str
    generator: str
    featured: bool = Field(default=False)
    image: uuid_lib.UUID = Field(default=None, foreign_key="image.id")
    is_locked: bool = Field(default=True)
    owner: uuid.UUID = Field(default=None, foreign_key=User.id)
    last_build_date: datetime.datetime
    feed_file_link: str


class ShowResponse(Show):
    duration: int
    episodes_number: int
    series: Optional[List[str]]


class ShowAdmin(ModelAdmin, model=Show):
    column_list = [Show.language,
                   Show.category,
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
