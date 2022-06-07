from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import UUIDModel, DeletableModel


class Series(UUIDModel, DeletableModel):
    __tablename__ = "series"

    name = Column(String)
    show_id = Column(UUID(as_uuid=True), ForeignKey("show.id"), index=True)
    show = relationship("Show", backref="series_arr", lazy="selectin", primaryjoin="Series.show_id == Show.id")
