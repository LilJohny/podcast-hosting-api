from typing import Type, Optional, List

from sqlalchemy.engine import Row
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import SQLModel

from settings import async_session_maker


async def save_entities(entities: List[SQLModel]):
    async with async_session_maker() as session:
        async with session.begin():
            for entity in entities:
                session.add(entity)
        await session.commit()


async def save_entity(entity: SQLModel):
    async with async_session_maker() as session:
        async with session.begin():
            session.add(entity)
        await session.commit()


def prepare_base_select(
        entity: Optional[Type[SQLModel]] = None,
        additional_columns: Optional[list] = None,
        only_columns: Optional[list] = None,
        join_models: Optional[List[Type[SQLModel]]] = None,
        additional_group_by_columns:Optional[list] = None
):
    if not only_columns:
        base_select = select(entity, *additional_columns) if additional_columns else select(entity)
    else:
        base_select = select(*only_columns)

    if join_models:
        for join_model in join_models:
            base_select = base_select.join(join_model, isouter=True)
    return base_select.group_by(entity.id) if not additional_group_by_columns else base_select.group_by(entity.id,*additional_group_by_columns)


async def get_entity(
        entity_id: uuid.UUID,
        entity: Optional[Type[SQLModel]] = None,
        additional_columns: Optional[list] = None,
        only_columns: Optional[list] = None,
        join_models: Optional[List[Type[SQLModel]]] = None,
        additional_group_by_columns: Optional[list] = None
) -> SQLModel:
    async with async_session_maker() as session:
        async with session.begin():
            base_select = prepare_base_select(entity, additional_columns, only_columns, join_models, additional_group_by_columns)
            result = await session.execute(
                base_select.filter(entity.id == entity_id).filter(entity.is_removed == False))
            item = result.first()
    return item


async def get_entities(
        entity: Type[SQLModel],
        conditions: Optional[List[BinaryExpression]] = None,
        additional_columns: Optional[list] = None,
        only_columns: Optional[list] = None,
        join_models: Optional[List[Type[SQLModel]]] = None,
        additional_group_by_columns: Optional[list] = None
) -> List[Row]:
    async with async_session_maker() as session:
        async with session.begin():
            base_select = prepare_base_select(entity, additional_columns, only_columns, join_models, additional_group_by_columns)

            query = base_select.filter(entity.is_removed == False)
            if conditions:
                for condition in conditions:
                    query = query.where(condition)
            result = await session.execute(query)

    return result.all()
