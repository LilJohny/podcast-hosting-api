from typing import Type, Union, List

from sqlmodel import SQLModel


def serialize(obj: Union[SQLModel, List[SQLModel]],
              serializer_class: Type[SQLModel],
              many: bool = False) -> Union[list, SQLModel]:
    return [serializer_class(**item.dict()) for item in obj] if many else serializer_class(**obj.dict())
