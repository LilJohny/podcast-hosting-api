import uuid

from sqlmodel import Field

from models import UUIDModel


class Series(UUIDModel, table=True):
    name: str = Field(nullable=False)
    show_id: uuid.UUID = Field(nullable=False, foreign_key="show.id")
