import uuid
from typing import Optional

from fastapi import status, APIRouter, Depends
from fastapi_pagination import Page, paginate, Params

from images.models import Image
from podcast_rss_generator import generate_new_show_rss_feed, PodcastOwnerDTO, ImageDTO
from settings import get_entity, save_entity, get_entities
from shows.models import ShowParam, Show, ShowResponse
from users import UserDB, current_active_user
from utils import serialize

shows_router = APIRouter(prefix="/shows")


@shows_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_show(show_param: ShowParam, user: UserDB = Depends(current_active_user)) -> ShowResponse:
    show = Show(**show_param.dict(), is_removed=False)
    image_data = await get_entity(str(show.image), Image)
    image = ImageDTO(title=image_data.title, url=image_data.file_url, height=100, width=100, link='')
    rss_feed = generate_new_show_rss_feed(show.title, '', '', show.description, 'LilJohny generator', show.language,
                                          show.show_copyright, show.last_build_date, image,
                                          PodcastOwnerDTO(name=user.email, email=user.email))
    print(rss_feed)
    await save_entity(show)
    return serialize(show, ShowResponse)


@shows_router.delete("/{show_id}")
async def delete_show(show_id: uuid.UUID):
    show = await get_entity(str(show_id), Show)
    show.is_removed = True
    await save_entity(show)
    return status.HTTP_202_ACCEPTED


@shows_router.put("/{show_id}")
async def update_show(show_id: uuid.UUID, show_param: ShowParam) -> ShowResponse:
    show = await get_entity(str(show_id), Show)
    show_data = show.dict()
    show_data.update(show_param.dict())
    show = Show(**show_data)
    await save_entity(show)
    return serialize(show, ShowResponse)


@shows_router.get("/{show_id}")
async def read_show(show_id: uuid.UUID) -> ShowResponse:
    show = await get_entity(str(show_id), Show)
    return serialize(show, ShowResponse)


@shows_router.get("/", response_model=Page[ShowResponse])
async def list_show(show_name: Optional[str] = None, featured: Optional[bool] = None, params: Params = Depends()):
    conditions = [(model_field == field_val) for model_field, field_val in [(Show.title, show_name),
                                                                            (Show.featured, featured)
                                                                            ] if field_val is not None]
    shows = await get_entities(Show, conditions)
    shows = serialize(shows, ShowResponse, many=True)
    return paginate(shows, params)


@shows_router.get("/my/all", response_model=Page[ShowResponse])
async def list_my_shows(params: Params = Depends(), user: UserDB = Depends(current_active_user)):
    shows = await get_entities(Show, [(Show.podcast_owner == str(user.id))])
    shows = serialize(shows, ShowResponse, many=True)
    return paginate(shows, params)
