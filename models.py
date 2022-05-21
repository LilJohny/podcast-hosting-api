import uuid as uuid_lib

from sqlmodel import SQLModel, Field


class DeletableModel(SQLModel):
    is_removed: bool

def str_uuid_factory():
    return str(uuid_lib.uuid4())

class UUIDModel(SQLModel):
    id: uuid_lib.UUID = Field(
        default_factory=str_uuid_factory,
        primary_key=True,
        index=True,
        nullable=False,
    )
