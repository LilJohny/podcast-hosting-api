import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, BOOLEAN, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from settings import Base
from shows.schemas import Category, Language
from utils.streamings import from_streaming_options_db


class Show(Base):
    __tablename__ = "show"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_removed = Column(BOOLEAN, default=False)
    title = Column(String)
    description = Column(String)
    language = Column(Enum(Language))
    show_copyright = Column(String)
    category = Column(Enum(Category))
    show_link = Column(String)
    media_link = Column(String)
    generator = Column(String)
    featured = Column(BOOLEAN, default=False)
    image = Column(String)
    is_locked = Column(BOOLEAN, default=True)
    owner = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    last_build_date = Column(DateTime)
    feed_file_link = Column(String)
    streaming_options = Column(String, default="000000")

    @hybrid_property
    def duration(self):
        return sum([episode.duration for episode in self.episodes])

    @hybrid_property
    def episodes_number(self):
        return len(self.episodes)

    @hybrid_property
    def selected_streamings(self):
        return from_streaming_options_db(self.streaming_options)
