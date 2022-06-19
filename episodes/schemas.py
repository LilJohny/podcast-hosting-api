import datetime
import enum
from uuid import UUID
from typing import Optional

from pydantic import Field

from podcast_rss_generator import EpisodeType
from schemas import UUIDSchema, DescribedSchema, TitledSchema
from pydantic import BaseModel



class EpisodeCreate(DescribedSchema, TitledSchema):
    episode_num: int
    season_num: int
    explicit: bool
    episode_type: EpisodeType
    show_id: UUID = Field(default=None, foreign_key="show.id")
    series: str = Field(default=None, nullable=True)
    file_link: str
    duration: int
    cover_image: UUID
    cover_link: str


class EpisodeUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    episode_num: Optional[int]
    season_num: Optional[int]
    explicit: Optional[bool]
    episode_type: Optional[EpisodeType]
    series: Optional[str] = Field(default=None, nullable=True)
    cover_image: Optional[UUID]


class EpisodeBase(EpisodeCreate):
    episode_link: str
    episode_guid: str
    pub_date: datetime.datetime


class EpisodeResponse(EpisodeBase, UUIDSchema):
    pass


class EpisodeFileUploadResponse(BaseModel):
    episode_link: str
    file_extension: str
    episode_duration: str
