from uuid import UUID

from fastapi_users import schemas


class UserRead(schemas.BaseUser[UUID]):
    first_name: str
    last_name: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
