from typing import Type, Optional, List

from sqlalchemy.future import select
from sqlmodel import SQLModel
from sqlalchemy.sql.elements import BinaryExpression
from settings import async_session_maker


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
