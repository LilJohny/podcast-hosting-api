import os
from typing import AsyncGenerator, Type, List, Optional

import aioboto3
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import SQLModel

DATABASE_URL = os.getenv('ASYNC_DATABASE_URL')
Base = declarative_base()
ENGINE = create_async_engine(DATABASE_URL)
BUCKET_NAME = os.getenv("BUCKETEER_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("BUCKETEER_AWS_ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.getenv("BUCKETEER_AWS_SECRET_ACCESS_KEY")
REGION = os.getenv("BUCKETEER_AWS_REGION")
aws_session = aioboto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name=REGION
)
PUBLIC_URL = os.getenv("PUBLIC_URL")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_BASE_URL = os.getenv("MAILGUN_BASE_URL")


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
            result = await session.execute(select(entity).filter_by(id=entity_id, is_removed=False))
            item = result.first()
    return item[0] if item else None


async def get_entities(entity: Type[SQLModel], conditions: Optional[List[BinaryExpression]] = None):
    async with async_session_maker() as session:
        async with session.begin():
            query = select(entity).filter_by(is_removed=False)
            if conditions:
                for condition in conditions:
                    query = query.where(condition)
            result = await session.execute(query)
    return [row[0] for row in result.all()]


async_session_maker = sessionmaker(ENGINE, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
