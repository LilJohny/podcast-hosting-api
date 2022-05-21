import dataclasses
from typing import Optional


@dataclasses.dataclass
class Image:
    url: str
    title: str
    link: str
    width: Optional[int] = None
    height: Optional[int] = None


@dataclasses.dataclass
class PodcastOwner:
    name: str
    email: str


@dataclasses.dataclass
class GUIDData:
    url: str
    isPermalink: bool
