import datetime
import enum
import uuid
from typing import Optional

from pydantic import Field

from schemas import UUIDSchema, DescribedSchema, TitledSchema
from pydantic import BaseModel


class EpisodeType(str, enum.Enum):
    full = "full"


class EpisodeCreate(DescribedSchema, TitledSchema):
    episode_num: int
    season_num: int
    explicit: bool
    episode_type: EpisodeType
    show_id: uuid.UUID = Field(default=None, foreign_key="show.id")
    series: str = Field(default=None, nullable=True)


class EpisodeUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    episode_num: Optional[int]
    season_num: Optional[int]
    explicit: Optional[bool]
    episode_type: Optional[EpisodeType]
    series: Optional[str] = Field(default=None, nullable=True)


class EpisodeBase(EpisodeCreate):
    file_link: str
    episode_link: str
    episode_guid: str
    pub_date: datetime.datetime
    duration: int


class EpisodeResponse(EpisodeBase, UUIDSchema):
    cover_link: str
