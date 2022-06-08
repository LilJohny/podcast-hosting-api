from sqlalchemy import Column, String, DateTime, ForeignKey, BOOLEAN, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from models import UUIDModel, DeletableModel, DescribedModel
from shows.schemas import Category, Language
from utils.streamings import from_streaming_options_db


class Show(UUIDModel, DeletableModel, DescribedModel):
    __tablename__ = "show"

    language = Column(Enum(Language))
    show_copyright = Column(String)
    category = Column(Enum(Category))
    show_link = Column(String)
    media_link = Column(String)
    generator = Column(String)
    featured = Column(BOOLEAN, default=False)
    image = Column(UUID(as_uuid=True), ForeignKey("image.id"), index=True)
    is_locked = Column(BOOLEAN, default=True)
    owner = Column(UUID(as_uuid=True), ForeignKey("user.id"), index=True)
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

    @hybrid_property
    def series_names(self):
        return sorted([series.name for series in self.series_arr])