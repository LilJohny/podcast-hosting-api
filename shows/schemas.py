import datetime
import enum
import uuid
import uuid as uuid_lib
from typing import Set, List, Optional

import sqlalchemy
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN
from sqlmodel import SQLModel, Field, Enum, Column
from models import DeletableModel, UUIDModel
from settings import Base
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
    selected_streamings: List[str]


class ShowUpdate(SQLModel):
    title: Optional[str]
    description: Optional[str]
    language: Optional[Language] = Field(sa_column=Column(Enum(Language)))
    show_copyright: Optional[str]
    category: Optional[Category] = Field(sa_column=Column(Enum(Category)))
    series: Optional[Set[str]]


# class Show(BaseShow, UUIDModel, DeletableModel, table=True):
#     show_link: str
#     media_link: str
#     generator: str
#     featured: bool = Field(default=False)
#     image: uuid_lib.UUID = Field(default=None, foreign_key="image.id")
#     is_locked: bool = Field(default=True)
#     owner: uuid.UUID = Field(default=None, foreign_key=User.id)
#     last_build_date: datetime.datetime
#     feed_file_link: str
#     streaming_options: str = Field(default="000000")


class ShowResponse(ShowCreate):
    duration: int
    episodes_number: int
    series: Optional[List[str]]
    selected_streamings: List[str]
