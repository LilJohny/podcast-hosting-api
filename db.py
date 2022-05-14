from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from images.models import Image

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
Base: DeclarativeMeta = declarative_base()
ENGINE = create_async_engine(DATABASE_URL)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def save_entity(entity: SQLModel, session: AsyncSession = Depends(get_async_session)):
    async with async_session_maker() as session:
        async with session.begin():
            session.add_all([entity])
        await session.commit()



async_session_maker = sessionmaker(ENGINE, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
