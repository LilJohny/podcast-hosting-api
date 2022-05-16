import datetime
import enum

from pydantic import HttpUrl
from sqlmodel import SQLModel, Field, Enum, Column

from models import UUIDModel, DeletableModel


class EpisodeType(str, enum.Enum):
    full = "full"


class EpisodeBase(SQLModel):
    title: str
    description: str
    episode_link: HttpUrl
    file_link: HttpUrl
    cover_image_link: HttpUrl
    episode_guid: str
    episode_num: int
    season_num: int
    explicit: bool
    pub_date: datetime.datetime
    duration: int
    episode_type: EpisodeType = Field(sa_column=Column(Enum(EpisodeType)))


class Episode(EpisodeBase, UUIDModel, DeletableModel, table=True):
    pass
