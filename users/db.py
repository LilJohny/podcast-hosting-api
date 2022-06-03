from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqladmin import ModelAdmin
from sqlalchemy import String, Column
from sqlalchemy.ext.asyncio import AsyncSession

from settings import Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name = Column(String)
    last_name = Column(String)

class UserAdmin(ModelAdmin, model=User):
    column_list = [User.id, User.first_name, User.last_name, User.email, User.is_active,
                   User.is_superuser, User.is_verified]

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
