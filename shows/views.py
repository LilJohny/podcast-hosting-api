import datetime
import uuid
from typing import Optional

from fastapi import status, APIRouter, Depends, UploadFile, File
from fastapi_pagination import Page, paginate, Params

from images.views import create_image
from models import str_uuid_factory
from podcast_rss_generator import generate_new_show_rss_feed, PodcastOwnerDTO, ImageDTO
from shows.db import save_entity, get_entities
from shows.models import ShowParam, Show, ShowResponse, ShowCreate
from users import UserDB, current_active_user
from utils.constants import GENERATOR_VERSION
from utils.rss import start_serving_rss_feed
from utils.serializers import serialize
from views import delete_entity, update_entity, read_entity

shows_router = APIRouter(prefix="/shows")


@shows_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_show(show_create_param: ShowCreate,
                      image_title: str,
                      image_file: UploadFile = File(...),
                      user: UserDB = Depends(current_active_user)) -> ShowResponse:
    image = await create_image(image_title, image_file)
    feed_file_link = "/".join([show_create_param.title, "feed.xml"])
    show_id = str_uuid_factory()
    show_link = "/".join([show_id, show_create_param.title])
    show = Show(**show_create_param.dict(),
                id=show_id,
                image=image.id,
                show_link=show_link,
                media_link=image.file_url,
                last_build_date=datetime.datetime.utcnow().replace(tzinfo=None),
                generator=GENERATOR_VERSION,
                owner=user.id,
                feed_file_link=feed_file_link)

    image = ImageDTO(title=image.title, url=image.file_url, height=100, width=100, link='')
    rss_feed = generate_new_show_rss_feed(show.title, '', '', show.description, GENERATOR_VERSION, show.language,
                                          show.show_copyright, show.last_build_date, image,
                                          PodcastOwnerDTO(name=user.email, email=user.email))
    start_serving_rss_feed(rss_feed, feed_file_link)
    await save_entity(show)
    return serialize(show, ShowResponse)


@shows_router.delete("/{show_id}")
async def delete_show(show_id: uuid.UUID):
    return await delete_entity(show_id, Show)


@shows_router.put("/{show_id}")
async def update_show(show_id: uuid.UUID, show_param: ShowParam) -> ShowResponse:
    show_param.last_build_date = show_param.last_build_date.replace(tzinfo=None)
    return await update_entity(show_id, Show, show_param, ShowResponse)


@shows_router.get("/{show_id}")
async def read_show(show_id: uuid.UUID) -> ShowResponse:
    return await read_entity(show_id, Show, ShowResponse)


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
    shows = await get_entities(Show, [(Show.owner == str(user.id))])
    shows = serialize(shows, ShowResponse, many=True)
    return paginate(shows, params)
