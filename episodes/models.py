import uuid

from sqlalchemy import Column, DateTime, Integer, String, BOOLEAN, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from episodes.schemas import EpisodeType
from settings import Base


class Episode(Base):
    __tablename__ = "episode"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_removed = Column(BOOLEAN, default=False)

    title = Column(String)
    description = Column(String)
    episode_num = Column(Integer)
    season_num = Column(Integer)
    explicit = Column(BOOLEAN)
    episode_type = Column(Enum(EpisodeType))
    show_id = Column(UUID(as_uuid=True), ForeignKey("show.id"))
    series = Column(String)
    file_link = Column(String)
    episode_link = Column(String)
    episode_guid = Column(String)
    pub_date = Column(DateTime)
    duration = Column(Integer)
    cover_image = Column(UUID(as_uuid=True), ForeignKey("image.id"))
    show = relationship("Show", backref="episodes", lazy="selectin", primaryjoin="Episode.show_id == Show.id")
