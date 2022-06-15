from uuid import UUID
from typing import Optional

from fastapi import HTTPException
from starlette import status

from utils.db import get_entity, save_entity


async def get_view_entity(entity_id: UUID, entity_class, opts: Optional[list] = None):
    entity = await get_entity(entity_id, entity_class, opts)
    if not entity:
        raise HTTPException(status_code=404, detail=f"{entity_class.__name__} not found")
    return entity


async def delete_entity(entity_id: UUID, entity_class):
    entity = await get_view_entity(entity_id, entity_class)
    entity.is_removed = True
    await save_entity(entity)
    return status.HTTP_202_ACCEPTED


async def update_entity(entity_id: UUID, entity_class, entity_param,  entity_instance=None, opts: Optional[list] = None):
    if not entity_instance:
        entity_instance = await get_view_entity(entity_id, entity_class, opts)
    for key, val in entity_param.items():
        setattr(entity_instance, key, val)
    await save_entity(entity_instance)
    return entity_instance


async def read_entity(entity_id: UUID, entity_class):
    entity = await get_view_entity(entity_id, entity_class)
    return entity
