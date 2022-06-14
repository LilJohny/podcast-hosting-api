import enum
import uuid
from typing import Set, List, Optional

from pydantic import BaseModel, Field

from schemas import UUIDSchema, DescribedSchema, TitledSchema


class Language(str, enum.Enum):
    english = "en"


class Category(str, enum.Enum):
    arts_books = "Arts/Books"


class BaseShow(DescribedSchema, TitledSchema):
    language: Language
    show_copyright: str
    category: Category
    series: Set[str]
    selected_streamings: List[str]


class ShowCreate(BaseShow):
    image_id: uuid.UUID


class ShowUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    language: Optional[Language]
    show_copyright: Optional[str]
    category: Optional[Category]
    series: Optional[Set[str]]


class ShowResponse(BaseShow, UUIDSchema):
    duration: int = Field(default=0)
    episodes_number: int = Field(default=0)
    series: Optional[List[str]]
    selected_streamings: List[str]
    image: uuid.UUID
    media_link: str
