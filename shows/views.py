import uuid
from typing import Optional

from fastapi import status, APIRouter, Depends, UploadFile, File
from fastapi_pagination import Page, paginate, Params

from images.models import Image
from images.views import create_image
from podcast_rss_generator import generate_new_show_rss_feed, PodcastOwnerDTO, ImageDTO
from shows.db import save_entity, get_entities
from shows.models import ShowParam, Show, ShowResponse, ShowCreate
from users import UserDB, current_active_user
from utils.files import upload_file_to_s3, FileKind, get_s3_key
from utils.serializers import serialize
from views import delete_entity, update_entity, read_entity, get_view_entity

shows_router = APIRouter(prefix="/shows")


@shows_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_show(show_create_param: ShowCreate, image_title: str, user: UserDB = Depends(current_active_user),
                      image_file: UploadFile = File(...), media_file: UploadFile = File(...)) -> ShowResponse:
    image = await create_image(image_title, image_file)
    s3_key = get_s3_key(media_file.filename, "audio")
    media_url = await upload_file_to_s3(s3_key, image_file.file, FileKind.AUDIO)
    show_create_param.last_build_date = show_create_param.last_build_date.replace(tzinfo=None)
    show = Show(**show_create_param.dict(), image=image.id, show_link="", media_link=media_url,
                feed_file_link="feed.xml", is_removed=False)
    image_data = await get_view_entity(show.image, Image)
    image = ImageDTO(title=image_data.title, url=image_data.file_url, height=100, width=100, link='')
    rss_feed = generate_new_show_rss_feed(show.title, '', '', show.description, 'LilJohny generator', show.language,
                                          show.show_copyright, show.last_build_date, image,
                                          PodcastOwnerDTO(name=user.email, email=user.email))
    print(rss_feed)
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
    shows = await get_entities(Show, [(Show.podcast_owner == str(user.id))])
    shows = serialize(shows, ShowResponse, many=True)
    return paginate(shows, params)
