import uuid

from sqlalchemy import Column, BOOLEAN, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from settings import Base


class Image(Base):
    __tablename__ = "image"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_removed = Column(BOOLEAN, default=False)
    title = Column(String)
    file_url = Column(String)
    show = relationship("Show", backref="cover_image",lazy="selectin", primaryjoin="Image.id == Show.image")