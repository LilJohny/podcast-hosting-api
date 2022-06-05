from typing import Type, Union, List

from sqlalchemy.engine import Row
from sqlmodel import SQLModel


def serialize(obj: Union[SQLModel, List[SQLModel], List[dict]],
              serializer_class: Type[SQLModel],
              many: bool = False) -> Union[list, SQLModel]:
    return [serializer_class(**unpack_obj(item)) for item in obj] if many else serializer_class(**obj.dict())


def unpack_obj(obj) -> dict:
    if isinstance(obj, SQLModel):
        return obj.dict()
    elif isinstance(obj, Row):
        return obj[0].dict()
    return obj


