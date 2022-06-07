import uuid

from sqlalchemy import Column, BOOLEAN, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from settings import BaseModel


class Image(BaseModel):
    __tablename__ = "image"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_removed = Column(BOOLEAN, default=False)
    title = Column(String)
    file_url = Column(String)
    episode = relationship("Episode", backref="image_val", lazy="selectin", primaryjoin="Image.id == Episode.cover_image")