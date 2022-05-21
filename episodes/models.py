import datetime
import enum
import uuid as uuid_lib

from pydantic import HttpUrl
from sqlmodel import SQLModel, Field, Enum, Column

from models import UUIDModel, DeletableModel


class EpisodeType(str, enum.Enum):
    full = "full"


class EpisodeParam(SQLModel):
    title: str
    description: str
    cover_image_link: HttpUrl
    episode_guid: str
    episode_num: int
    season_num: int
    explicit: bool
    pub_date: datetime.datetime
    duration: int
    episode_type: EpisodeType = Field(sa_column=Column(Enum(EpisodeType)))
    show_id: uuid_lib.UUID = Field(default=None, foreign_key="show.id")
    series: str = Field(default=None, nullable=True)


class EpisodeResponse(EpisodeParam, UUIDModel):
    file_link: HttpUrl
    episode_link: HttpUrl


class Episode(EpisodeResponse, DeletableModel, table=True):
    pass
