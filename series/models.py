import uuid

from sqlmodel import Field

from models import UUIDModel
from shows.models import Show


class Series(UUIDModel, table=True):
    name: str = Field(primary_key=True, nullable=False)
    show_id: uuid.UUID = Field(nullable=False, foreign_key=Show.id)
