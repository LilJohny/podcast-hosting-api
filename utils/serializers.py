from typing import Type, Union

from sqlmodel import SQLModel


def serialize(obj: Union[SQLModel, list[SQLModel]], serializer_class: Type[SQLModel], many: bool = False) -> list:
    return [serializer_class(**item.dict()) for item in obj] if many else serializer_class(**obj.dict())
