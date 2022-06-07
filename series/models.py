import uuid

from sqlalchemy import Column, String, BOOLEAN, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from settings import BaseModel


class Series(BaseModel):
    __tablename__ = "series"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_removed = Column(BOOLEAN, default=False)
    name = Column(String)
    show_id = Column(UUID(as_uuid=True), ForeignKey("show.id"), index=True)
    show = relationship("Show", backref="series_arr", lazy="selectin", primaryjoin="Series.show_id == Show.id")
