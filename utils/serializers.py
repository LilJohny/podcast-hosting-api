from typing import Type, Union, List

from sqlalchemy.engine import Row

from settings import BaseModel


def serialize(
        obj: Union[BaseModel, List[BaseModel], List[dict], dict],
        serializer_class: Type[BaseModel],
        many: bool = False
) -> Union[list, BaseModel]:
    return [serializer_class(**unpack_obj(item)) for item in obj] if many else serializer_class(**unpack_obj(obj))


def unpack_obj(obj) -> dict:
    if isinstance(obj, BaseModel):
        return obj.dict()
    elif isinstance(obj, Row):
        return obj[0].dict()
    return obj
