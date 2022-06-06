import datetime
import uuid
from typing import Optional

from fastapi import status, APIRouter, Depends, UploadFile, File
from fastapi_pagination import Page, paginate
from sqlalchemy.sql import functions as sql_functions

from episodes.models import Episode
from images.views import create_image
from models import str_uuid_factory
from podcast_rss_generator import generate_new_show_rss_feed, PodcastOwnerDTO, ImageDTO
from series.models import Series
from series.views import create_series_batch
from shows.models import ShowUpdate, Show, ShowResponse, ShowCreate
from users import User, current_active_user
from utils.constants import GENERATOR_VERSION
from utils.db import save_entity, get_entities, get_entity
from utils.files import upload_file_to_s3, FileKind
from utils.serializers import serialize
from utils.streamings import to_streaming_options_db, from_streaming_options_db
from views import delete_entity, update_entity

shows_router = APIRouter(prefix="/shows")


@shows_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_show(show_create_param: ShowCreate,
                      image_title: str,
                      image_file: UploadFile = File(...),
                      user: User = Depends(current_active_user)) -> ShowResponse:
    image = await create_image(image_title, image_file)
    show_id = str_uuid_factory()
    show_link = "/".join([show_id, show_create_param.title])
    image_dto = ImageDTO(title=image.title, url=image.file_url, height=100, width=100, link='')
    rss_feed = generate_new_show_rss_feed(show_create_param.title,
                                          '',
                                          '',
                                          show_create_param.description,
                                          GENERATOR_VERSION,
                                          show_create_param.language,
                                          show_create_param.show_copyright,
                                          datetime.datetime.utcnow().replace(
                                              tzinfo=None
                                          ),
                                          image_dto,
                                          PodcastOwnerDTO(name=user.email, email=user.email))
    feed_file_link = await upload_file_to_s3(f"{show_id.replace('-', '')}.xml", rss_feed.decode('utf-8'), FileKind.XML)

    show_create_param_data = show_create_param.dict()

    series_param = show_create_param_data.pop("series")
    selected_streamings = show_create_param_data.pop("selected_streamings")
    show = Show(
        **show_create_param_data,
        id=show_id,
        image=image.id,
        show_link=show_link,
        media_link=image.file_url,
        last_build_date=datetime.datetime.utcnow().replace(tzinfo=None),
        generator=GENERATOR_VERSION,
        owner=user.id,
        feed_file_link=feed_file_link,
        streaming_options=to_streaming_options_db(selected_streamings)
    )
    await save_entity(show)
    await create_series_batch(show_id, series_param)
    return ShowResponse(**show.dict(), series=series_param, selected_streamings=selected_streamings)


@shows_router.get("/my", response_model=Page[ShowResponse])
async def list_my_shows(
        show_name: Optional[str] = None,
        featured: Optional[bool] = None,
        user: User = Depends(current_active_user)
) -> Page[ShowResponse]:
    conditions = [
        (model_field == field_val) for model_field, field_val in [
            (Show.featured, featured),
            (Show.owner, user.id)
        ] if field_val is not None
    ]

    if show_name:
        conditions.append(Show.title.ilike(show_name))

    shows = await list_shows(conditions)
    return paginate(shows)


@shows_router.delete("/{show_id}")
async def delete_show(show_id: uuid.UUID):
    return await delete_entity(show_id, Show)


@shows_router.put("/{show_id}")
async def update_show(show_id: uuid.UUID, show_param: ShowUpdate) -> ShowResponse:
    show_param.last_build_date = show_param.last_build_date.replace(tzinfo=None)
    return await update_entity(show_id, Show, show_param, ShowResponse)


@shows_router.get("/{show_id}")
async def read_show(show_id: uuid.UUID) -> ShowResponse:
    show = await get_entity(
        show_id,
        Show,
        additional_columns=[sql_functions.array_agg(Series.name)],
        join_models=[Series]
    )
    return ShowResponse(
        **show[0].dict(),
        series=show[1],
        selected_streamings=from_streaming_options_db(show[0].streaming_options)
    )


@shows_router.get("/", response_model=Page[ShowResponse])
async def list_all_shows(show_name: Optional[str] = None, featured: Optional[bool] = None):
    conditions = []
    if featured:
        conditions.append(Show.featured == featured)
    if show_name:
        conditions.append(Show.title.ilike(show_name))
    shows = await list_shows(conditions)
    return paginate(shows)


async def list_shows(conditions):
    shows_episodes = await get_entities(
        Show,
        conditions,
        additional_columns=[
            sql_functions.count(Episode.id.distinct()),
            sql_functions.coalesce(sql_functions.sum(Episode.duration), 0)
        ],
        join_models=[Episode],
    )
    series = await get_entities(Show, conditions, only_columns=[Show.id, sql_functions.array_agg(Series.name.distinct())], join_models=[Series])

    shows = [ShowResponse(
        **show_fields[0][0].dict(),
        episodes_number=show_fields[0][1],
        duration=show_fields[0][2],
        series=show_fields[1][1],
        selected_streamings=from_streaming_options_db(shows_episodes[0][0].streaming_options)
    ) for show_fields in zip(shows_episodes, series)]
    return shows
