from typing import Optional

from fastapi_users import models


class UserParam(models.BaseUser):
    first_name: str
    last_name: str


class UserCreate(models.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(models.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]


class UserDB(UserParam, models.BaseUserDB):
    pass
