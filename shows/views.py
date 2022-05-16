import uuid
from fastapi import status, APIRouter

from db import get_entity, save_entity
from shows.models import ShowBase, Show

shows_router = APIRouter(prefix="/shows")


@shows_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_show(show_param: ShowBase) -> ShowBase:
    show = Show(**show_param.dict(), is_removed=False, id=str(uuid.uuid4()))
    await save_entity(show)
    return show


@shows_router.delete("/{show_id}")
async def delete_show(show_id: str):
    show = await get_entity(show_id, Show)
    show.is_removed = True
    await save_entity(show)
    return status.HTTP_202_ACCEPTED


@shows_router.put("/{show_id}")
async def update_show(show_id: str, show_param: ShowBase) -> Show:
    show = await get_entity(show_id, Show)
    show_data = show.dict()
    show_data.update(show_param.dict())
    show = Show(**show_data)
    await save_entity(show)
    return show


@shows_router.get("/{show_id}")
async def read_show(show_id: str) -> ShowBase:
    image = await get_entity(show_id, Show)
    return ShowBase(**image.dict())


@shows_router.get("/")
def list_show():
    pass
