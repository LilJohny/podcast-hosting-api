import datetime
import enum
import uuid as uuid_lib

from sqladmin import ModelAdmin
from sqlmodel import SQLModel, Field, Enum, Column

from models import UUIDModel, DeletableModel


class EpisodeType(str, enum.Enum):
    full = "full"


class EpisodeParam(SQLModel):
    title: str
    description: str
    episode_num: int
    season_num: int
    explicit: bool
    episode_type: EpisodeType = Field(sa_column=Column(Enum(EpisodeType)))
    show_id: uuid_lib.UUID = Field(default=None, foreign_key="show.id")
    series: str = Field(default=None, nullable=True)


class EpisodeBase(EpisodeParam):
    file_link: str
    episode_link: str
    episode_guid: str
    pub_date: datetime.datetime
    duration: int


class EpisodeResponse(EpisodeBase, UUIDModel):
    cover_link: str


class Episode(EpisodeBase, UUIDModel, DeletableModel, table=True):
    cover_image: uuid_lib.UUID = Field(default=None, foreign_key="image.id")
