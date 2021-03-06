from typing import Optional
from uuid import UUID

from fastapi import status, APIRouter, Depends
from fastapi_pagination import Page, create_page
from sqlalchemy import desc
from sqlalchemy.orm import selectinload

from images.models import Image
from podcast_rss_generator.generators import generate_new_show_feed
from series.models import Series
from series.views import create_series_batch
from shows.models import Show
from shows.schemas import ShowUpdate, ShowResponse, ShowCreate
from users import User, current_active_user
from utils.column_factories import str_uuid_factory
from utils.db import save_entity, get_entities, get_entity, delete_entities_permanent
from utils.links import get_feed_link, get_show_link
from utils.streamings import to_streaming_options_db
from views import delete_entity, update_entity, get_view_entity

shows_router = APIRouter(prefix="/shows")


@shows_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ShowResponse)
async def create_show(
        show_create_param: ShowCreate,
        user: User = Depends(current_active_user)
) -> ShowResponse:
    show_id = str_uuid_factory()
    show_link, show_feed_link = get_show_link(show_id), get_feed_link(show_id)

    image = await get_entity(show_create_param.image, Image)

    rss_file_link = await generate_new_show_feed(image, show_create_param, show_link, show_feed_link, show_id, user)

    show_create_param_data = show_create_param.dict()

    series_param, selected_streamings = show_create_param_data.pop("series"), \
                                        show_create_param_data.pop("selected_streamings")

    show = Show(
        **show_create_param_data,
        id=show_id,
        show_link=show_link,
        media_link=image.file_url,
        owner=user.id,
        feed_file_link=rss_file_link,
        streaming_options=to_streaming_options_db(selected_streamings)
    )

    await save_entity(show)
    await create_series_batch(show_id, series_param)

    return ShowResponse(
        **show.__dict__,
        series=series_param,
        selected_streamings=selected_streamings,
        cover_link=image.file_url,
        feed_link=show_feed_link
    )


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
        conditions.append(Show.title.ilike(f"%{show_name}%"))

    return await list_shows(conditions)


@shows_router.delete("/{show_id}")
async def delete_show(
        show_id: UUID,
        user: User = Depends(current_active_user)
):
    return await delete_entity(show_id, Show)


@shows_router.put("/{show_id}")
async def update_show(
        show_id: UUID,
        show_param: ShowUpdate,
        user: User = Depends(current_active_user)
) -> int:
    show_param_data = show_param.dict()
    show_param_data = {key: show_param_data[key] for key in show_param_data if show_param_data[key]}

    selected_streamings_param, series_param, image_param = show_param_data.pop("selected_streamings", None), \
                                                           show_param_data.pop("series", None), \
                                                           show_param_data.get("image", None)

    if selected_streamings_param:
        show_param_data["streaming_options"] = to_streaming_options_db(selected_streamings_param)
    if image_param:
        show_param_data["media_link"] = await get_entity(image_param, Image, only_columns=[Image.file_url])

    show = await get_view_entity(show_id, Show, opts=[selectinload(Show.series_arr), selectinload(Show.episodes)])
    if series_param:
        series_param = sorted(series_param)
        absent_series = [series.id for series in show.series_arr if series.name not in series_param]
        await delete_entities_permanent(absent_series, Series)

        series_to_create = [series_new for series_new in series_param if series_new not in show.series_names]
        await create_series_batch(show.id, series_to_create)

    await update_entity(show_id, Show, show_param_data, entity_instance=show)

    return status.HTTP_202_ACCEPTED


@shows_router.get("/{show_id}", response_model=ShowResponse)
async def read_show(
        show_id: UUID,
        user: User = Depends(current_active_user)
) -> ShowResponse:
    show = await get_entity(
        show_id,
        Show,
        opts=[
            selectinload(Show.series_arr),
            selectinload(Show.episodes),
        ]
    )
    return ShowResponse(
        **show.__dict__,
        duration=show.duration,
        episodes_number=show.episodes_number,
        series=show.series_names,
        selected_streamings=show.selected_streamings,
        feed_link=get_feed_link(show_id)
    )


@shows_router.get("/", response_model=Page[ShowResponse])
async def list_all_shows(
        show_name: Optional[str] = None,
        featured: Optional[bool] = None
):
    conditions = []
    if featured:
        conditions.append(Show.featured == featured)
    if show_name:
        conditions.append(Show.title.ilike(show_name))
    return await list_shows(conditions)


async def list_shows(conditions):
    shows, total, params = await get_entities(
        Show,
        conditions,
        opts=[
            selectinload(Show.series_arr),
            selectinload(Show.episodes)
        ],
        order_by=lambda: desc(Show.last_build_date),
        pagination=True
    )

    shows = [
        ShowResponse(
            **show[0].__dict__,
            duration=show[0].duration,
            episodes_number=show[0].episodes_number,
            series=show[0].series_names,
            selected_streamings=show[0].selected_streamings
        ) for show in shows]

    shows_page = create_page(shows, total, params)
    return shows_page
