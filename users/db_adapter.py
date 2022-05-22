from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncSession

from settings import get_async_session, Base
from .authentication.models import AccessToken
from .models import UserDB


class UserTable(Base, SQLAlchemyBaseUserTable):
    first_name = Column(String)
    last_name = Column(String)


class AccessTokenTable(SQLAlchemyBaseAccessTokenTable, Base):
    pass


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(UserDB, session, UserTable)


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(AccessToken, session, AccessTokenTable)
