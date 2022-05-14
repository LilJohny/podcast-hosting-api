import datetime

from sqlmodel import SQLModel, Field, Boolean, DateTime


class ShowBase(SQLModel):
    title: str
    podcast_link: str
    media_link: str
    description: str
    generator: str
    language: str
    show_copyright: str
    last_build_date: datetime.datetime
    image: str
    podcast_owner: str
    is_locked: bool
    category: str


class Show(ShowBase, table=True):
    id:int = Field(default=None, primary_key=True)


