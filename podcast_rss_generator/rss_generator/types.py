import dataclasses
from typing import Optional


@dataclasses.dataclass
class ImageDTO:
    url: str
    title: str
    link: str
    width: Optional[int] = None
    height: Optional[int] = None


@dataclasses.dataclass
class PodcastOwnerDTO:
    name: str
    email: str


@dataclasses.dataclass
class GUIDDataDTO:
    url: str
    isPermalink: bool
