import datetime
import enum
import uuid

from pydantic import BaseModel, Field

from schemas import UUIDModel


class EpisodeType(str, enum.Enum):
    full = "full"


class EpisodeCreate(BaseModel):
    title: str
    description: str
    episode_num: int
    season_num: int
    explicit: bool
    episode_type: EpisodeType
    show_id: uuid.UUID = Field(default=None, foreign_key="show.id")
    series: str = Field(default=None, nullable=True)


class EpisodeUpdate(EpisodeCreate):
    pass


class EpisodeBase(EpisodeCreate):
    file_link: str
    episode_link: str
    episode_guid: str
    pub_date: datetime.datetime
    duration: int


class EpisodeResponse(EpisodeBase, UUIDModel):
    cover_link: str
