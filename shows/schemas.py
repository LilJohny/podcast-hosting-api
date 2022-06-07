import enum
import uuid
from typing import Set, List, Optional

from pydantic import BaseModel
from schemas import UUIDModel


class Language(str, enum.Enum):
    english = "en"


class Category(str, enum.Enum):
    arts_books = "Arts/Books"


class BaseShow(BaseModel):
    title: str
    description: str
    language: Language
    show_copyright: str
    category: Category


class ShowCreate(BaseShow):
    series: Set[str]
    selected_streamings: List[str]


class ShowUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    language: Optional[Language]
    show_copyright: Optional[str]
    category: Optional[Category]
    series: Optional[Set[str]]


class ShowResponse(ShowCreate, UUIDModel):
    duration: int
    episodes_number: int
    series: Optional[List[str]]
    selected_streamings: List[str]
    image: uuid.UUID
