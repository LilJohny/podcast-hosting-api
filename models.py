import uuid as uuid_lib

from sqlmodel import SQLModel, Field


class DeletableModel(SQLModel):
    is_removed: bool


class UUIDModel(SQLModel):
    id: str = Field(
        default_factory=uuid_lib.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
