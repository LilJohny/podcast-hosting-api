import uuid as uuid_lib

from pydantic import Field, BaseModel


class UUIDSchema(BaseModel):
    id: uuid_lib.UUID = Field(
        primary_key=True,
        index=True,
        nullable=False,
    )


class DescribedSchema(BaseModel):
    description: str


class TitledSchema(BaseModel):
    title: str
