from uuid import UUID
from typing import Type, Optional, List, Callable

import sqlalchemy
from fastapi_pagination import Page
from sqlalchemy.future import select
from sqlalchemy.sql.elements import BinaryExpression

from settings import async_session_maker, BaseModel
from utils.pagination import paginate


async def save_entities(entities: List[BaseModel]):
    async with async_session_maker() as session:
        async with session.begin():
            for entity in entities:
                session.add(entity)
        await session.commit()


async def save_entity(entity: BaseModel):
    async with async_session_maker() as session:
        async with session.begin():
            session.add(entity)
        await session.commit()


def prepare_base_select(
        entity: Type[BaseModel],
        additional_group_by_columns: Optional[list] = None,
        opts: Optional[list] = None,
        order_by: Optional[Callable] = None,
        only_columns: Optional[list] = None
):
    if not only_columns:
        base_select = select(entity)
    else:
        base_select = select(*only_columns)

    if opts:
        for opt in opts:
            base_select = base_select.options(opt)
    base_select = base_select.group_by(entity.id) \
        if not additional_group_by_columns \
        else base_select.group_by(entity.id, *additional_group_by_columns)
    if not order_by:
        order_by = entity.id
    return base_select.order_by(order_by) if order_by else base_select.order_by(entity.id)


async def get_entity(
        entity_id: UUID,
        entity: Type[BaseModel],
        opts: Optional[list] = None,
        only_columns: Optional[list] = None
) -> BaseModel:
    async with async_session_maker() as session:
        base_select = prepare_base_select(entity, opts=opts, only_columns=only_columns)
        result = await session.execute(
            base_select.filter(entity.id == entity_id).filter(entity.is_removed == False))
        item = result.first()
    return item[0]


async def get_entities(
        entity: Type[BaseModel],
        conditions: Optional[List[BinaryExpression]] = None,
        additional_group_by_columns: Optional[list] = None,
        opts: list = None,
        order_by: Optional[Callable] = None,
        pagination: bool = False
) -> Page:
    async with async_session_maker() as session:
        base_select = prepare_base_select(entity, additional_group_by_columns, opts, order_by)

        query = base_select.filter(entity.is_removed == False)
        if conditions:
            for condition in conditions:
                query = query.where(condition)

        if pagination:
            entities = await paginate(session, query)
        else:
            result = await session.execute(query)
            entities = result.all()

    return entities


async def delete_entity_permanent(
        entity_id: UUID,
        entity: Type[BaseModel]
):
    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(sqlalchemy.delete(entity).where(entity.id == entity_id))
            await session.commit()


async def delete_entities_permanent(
        entity_ids: List[UUID],
        entity: Type[BaseModel]
):
    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(sqlalchemy.delete(entity).where(entity.id.in_(entity_ids)))
            await session.commit()
