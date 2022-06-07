import uuid

from sqlalchemy import Column, BOOLEAN, String
from sqlalchemy.dialects.postgresql import UUID

from settings import BaseModel


class UUIDModel(BaseModel):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class DeletableModel(BaseModel):
    __abstract__ = True
    is_removed = Column(BOOLEAN, default=False)


class DescribedModel(BaseModel):
    __abstract__ = True
    title = Column(String)
    description = Column(String)
