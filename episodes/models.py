from sqlalchemy import Column, DateTime, Integer, String, BOOLEAN, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from episodes.schemas import EpisodeType
from models import UUIDModel, DescribedModel, DeletableModel
from utils.column_factories import datetime_now_no_tz, str_uuid_factory


class Episode(UUIDModel, DeletableModel, DescribedModel):
    __tablename__ = "episode"

    episode_num = Column(Integer)
    season_num = Column(Integer)
    explicit = Column(BOOLEAN)
    episode_type = Column(Enum(EpisodeType))
    show_id = Column(UUID(as_uuid=True), ForeignKey("show.id"), index=True)
    series = Column(String)
    file_link = Column(String)
    episode_link = Column(String)
    episode_guid = Column(String, default=str_uuid_factory)
    pub_date = Column(DateTime, default=datetime_now_no_tz, onupdate=datetime_now_no_tz)
    duration = Column(Integer)
    cover_image = Column(UUID(as_uuid=True), ForeignKey("image.id"))
    show = relationship("Show", backref="episodes", lazy="selectin", primaryjoin="Episode.show_id == Show.id")
