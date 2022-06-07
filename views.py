import uuid

from fastapi import HTTPException
from starlette import status

from utils.db import get_entity, save_entity
from utils.serializers import serialize


async def get_view_entity(entity_id: uuid.UUID, entity_class):
    entity_id = str(entity_id)
    entity = await get_entity(entity_id, entity_class)
    if not entity:
        raise HTTPException(status_code=404, detail=f"{entity_class.__name__} not found")
    return entity


async def delete_entity(entity_id: uuid.UUID, entity_class):
    entity = await get_view_entity(entity_id, entity_class)
    entity.is_removed = True
    await save_entity(entity)
    return status.HTTP_202_ACCEPTED


async def update_entity(entity_id: uuid.UUID, entity_class, entity_param, serializer_class):
    entity = await get_view_entity(entity_id, entity_class)
    for key, val in entity_param.dict().items():
        setattr(entity, key, val)
    await save_entity(entity)
    return serialize(entity, serializer_class)


async def read_entity(entity_id: uuid.UUID, entity_class, serializer_class):
    entity = await get_view_entity(entity_id, entity_class)
    return entity
