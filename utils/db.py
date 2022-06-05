from typing import Type, Optional, List

from sqlalchemy.engine import Row
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import SQLModel

from settings import async_session_maker


async def save_entity(entity: SQLModel):
    async with async_session_maker() as session:
        async with session.begin():
            session.add(entity)
        await session.commit()


def prepare_base_select(
        entity: Optional[Type[SQLModel]] = None,
        additional_columns: Optional[list] = None,
        only_columns: Optional[list] = None,
        join_model: Optional[Type[SQLModel]] = None
):
    if not only_columns:
        base_select = select(entity, *additional_columns) if additional_columns else select(entity)
    else:
        base_select = select(*only_columns)

    if join_model:
        base_select = base_select.join(join_model, isouter=True).group_by(entity.id)
    return base_select


async def get_entity(
        entity_id: str,
        entity: Optional[Type[SQLModel]] = None,
        additional_columns: Optional[list] = None,
        only_columns: Optional[list] = None,
        join_model: Optional[Type[SQLModel]] = None
) -> SQLModel:
    async with async_session_maker() as session:
        async with session.begin():
            base_select = prepare_base_select(entity, additional_columns, only_columns, join_model)
            result = await session.execute(
                base_select.filter(entity.id == entity_id).filter(entity.is_removed == False))
            item = result.first()
    return item[0] if item else None


async def get_entities(
        entity: Type[SQLModel],
        conditions: Optional[List[BinaryExpression]] = None,
        additional_columns: Optional[list] = None,
        only_columns: Optional[list] = None,
        join_model: Optional[Type[SQLModel]] = None
) -> List[Row]:
    async with async_session_maker() as session:
        async with session.begin():
            base_select = prepare_base_select(entity, additional_columns, only_columns, join_model)

            query = base_select.filter(entity.is_removed == False)
            if conditions:
                for condition in conditions:
                    query = query.where(condition)
            result = await session.execute(query)

    return result.all()
