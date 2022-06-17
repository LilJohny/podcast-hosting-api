from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import UUIDModel, DeletableModel


class Image(UUIDModel, DeletableModel):
    __tablename__ = "image"

    title = Column(String)
    file_url = Column(String)
    episode = relationship(
        "Episode",
        backref="image_val",
        lazy="selectin",
        primaryjoin="Image.id == Episode.cover_image"
    )
