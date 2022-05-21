import os
from typing import AsyncGenerator, Type, List, Optional

import aioboto3
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import SQLModel

DATABASE_URL = os.getenv('ASYNC_DATABASE_URL')
Base: DeclarativeMeta = declarative_base()
ENGINE = create_async_engine(DATABASE_URL)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def save_entity(entity: SQLModel):
    async with async_session_maker() as session:
        async with session.begin():
            session.add(entity)
        await session.commit()


async def get_entity(entity_id: str, entity: Type[SQLModel]):
    async with async_session_maker() as session:
        async with session.begin():
            result = await session.execute(select(entity).filter_by(id=entity_id))
            return result.first()[0]


async def get_entities(entity: Type[SQLModel], conditions: Optional[List[BinaryExpression]]=None):
    async with async_session_maker() as session:
        async with session.begin():
            query = select(entity)
            if conditions:
                for condition in conditions:
                    query = query.where(condition)
            result = await session.execute(query)
    return [row[0] for row in result.all()]


async_session_maker = sessionmaker(ENGINE, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)