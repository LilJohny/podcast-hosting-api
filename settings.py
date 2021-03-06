import os
from typing import AsyncGenerator

import aioboto3
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL = DATABASE_URL.replace('postgres', 'postgresql+asyncpg')
BaseModel = declarative_base()
ENGINE = create_async_engine(DATABASE_URL)
BUCKET_NAME = os.getenv("BUCKETEER_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("BUCKETEER_AWS_ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.getenv("BUCKETEER_AWS_SECRET_ACCESS_KEY")
REGION = os.getenv("BUCKETEER_AWS_REGION")
BASE_URL = os.getenv("BASE_URL")
aws_session = aioboto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    region_name=REGION
)
PUBLIC_URL = os.getenv("PUBLIC_URL")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_BASE_URL = os.getenv("MAILGUN_BASE_URL")
SSH_PUBLIC_KEY = os.getenv("SSH_PUBLIC_KEY")
SSH_PRIVATE_KEY = os.getenv("SSH_PRIVATE_KEY")
USER_MANAGER_SECRET = os.getenv("USER_MANAGER_SECRET")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async_session_maker = sessionmaker(ENGINE, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with ENGINE.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
