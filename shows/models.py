import datetime
import uuid as uuid_lib
from pydantic import AnyUrl, Json, FileUrl
from sqlmodel import SQLModel, Field, Enum, Column
import enum


class Language(str, enum.Enum):
    english = "en"


class Category(str, enum.Enum):
    arts_books = "Arts/Books"


class ImageBase(SQLModel):
    file_url: FileUrl
    title: str
    show_link: AnyUrl = Field(default=None, foreign_key="show.show_link")


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


class Image(ImageBase, table=True):
    id: uuid_lib.UUID = Field(
        default_factory=uuid_lib.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


class Show(ShowBase, table=True):
    id: uuid_lib.UUID = Field(
        default_factory=uuid_lib.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    image: uuid_lib.UUID = Field(default=None, foreign_key="image.id")
