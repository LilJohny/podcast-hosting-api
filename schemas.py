import uuid as uuid_lib

from pydantic import Field, BaseModel

class DeletableModel(BaseModel):
    is_removed: bool = Field(default=False)


def str_uuid_factory():
    return str(uuid_lib.uuid4())


class UUIDModel(BaseModel):
    id: uuid_lib.UUID = Field(
        primary_key=True,
        index=True,
        nullable=False,
    )
