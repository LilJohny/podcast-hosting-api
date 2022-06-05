import uuid
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from shows.models import Show


class Series(SQLModel, table=True):
    name: str = Field(primary_key=True, nullable=False)
    show_id: uuid.UUID = Field(nullable=False, foreign_key=Show.id)
    show: Optional[Show] = Relationship(back_populates="series_lst")