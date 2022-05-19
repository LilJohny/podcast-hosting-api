import uuid
from typing import List, Optional

from fastapi import status, APIRouter, Depends
from fastapi_pagination import Page, paginate, Params

from db import get_entity, save_entity, get_entities
from shows.models import ShowDTO, Show
from users import UserDB, current_active_user

shows_router = APIRouter(prefix="/shows")


@shows_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_show(show_param: ShowDTO) -> ShowDTO:
    show = Show(**show_param.dict(), is_removed=False)
    await save_entity(show)
    return show


@shows_router.delete("/{show_id}")
async def delete_show(show_id: uuid.UUID):
    show = await get_entity(str(show_id), Show)
    show.is_removed = True
    await save_entity(show)
    return status.HTTP_202_ACCEPTED


@shows_router.put("/{show_id}")
async def update_show(show_id: uuid.UUID, show_param: ShowDTO) -> Show:
    show = await get_entity(str(show_id), Show)
    show_data = show.dict()
    show_data.update(show_param.dict())
    show = Show(**show_data)
    await save_entity(show)
    return show


@shows_router.get("/{show_id}")
async def read_show(show_id: uuid.UUID) -> ShowDTO:
    show = await get_entity(str(show_id), Show)
    return ShowDTO(**show.dict())


@shows_router.get("/", response_model=Page[ShowDTO])
async def list_show(show_name: Optional[str] = None, params: Params = Depends()):
    filtering_condition = Show.title == show_name if show_name else None
    shows = await get_entities(Show, [filtering_condition])
    return paginate(shows, params)


@shows_router.get("/my/all", response_model=Page[Show])
async def shows_my(params: Params = Depends(), user: UserDB = Depends(current_active_user)):
    shows = await get_entities(Show, [(Show.podcast_owner == str(user.id))])
    return paginate(shows, params)


@shows_router.get('/featured')
async def featured_shows() -> List[Show]:
    pass
