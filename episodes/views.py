import datetime
import os
import uuid
from typing import Optional

from fastapi import APIRouter, status, UploadFile, File, HTTPException
from fastapi_pagination import Page, create_page
from sqlalchemy.orm import selectinload

from episodes.models import Episode
from episodes.schemas import EpisodeCreate, EpisodeResponse, EpisodeUpdate
from images.views import create_image
from schemas import str_uuid_factory
from utils.audio import DURATION_FINDERS
from utils.db import save_entity, get_entities_paginated, get_entity
from utils.files import upload_file_to_s3, FileKind, get_s3_key
from views import delete_entity, update_entity

episodes_router = APIRouter(prefix="/episodes")


@episodes_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_episode(episode_param: EpisodeCreate,
                         image_title: str,
                         episode_file: UploadFile = File(...),
                         image_file: UploadFile = File(...)) -> EpisodeResponse:
    image = await create_image(image_title, image_file)
    image_s3_key = get_s3_key(episode_file.filename, episode_param.title)
    episode_link = await upload_file_to_s3(image_s3_key, episode_file.file,
                                           FileKind.AUDIO)
    episode_id = str_uuid_factory()
    _, file_extension = os.path.splitext(episode_file.filename)
    duration_finder = DURATION_FINDERS.get(file_extension)
    if duration_finder is None:
        raise HTTPException(status_code=400, detail="Amphora supports only .mp3 and .wave audio formats")
    episode_duration = duration_finder(episode_file.file)
    episode = Episode(**episode_param.dict(),
                      id=episode_id,
                      file_link=episode_link,
                      episode_link=f"/episode_id",
                      cover_image=image.id,
                      episode_guid=str_uuid_factory(),
                      pub_date=datetime.datetime.utcnow().replace(tzinfo=None),
                      duration=episode_duration
                      )
    await save_entity(episode)
    return EpisodeResponse(
        **episode.__dict__,
        cover_link=image.file_url
    )


@episodes_router.delete("/{episode_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_episode(episode_id: uuid.UUID):
    return await delete_entity(episode_id, Episode)


@episodes_router.put("/{episode_id}", status_code=status.HTTP_200_OK)
async def update_episode(episode_id: uuid.UUID, episode_param: EpisodeUpdate) -> EpisodeResponse:
    return await update_entity(episode_id, Episode, episode_param, EpisodeResponse)


@episodes_router.get("/{episode_id}")
async def read_episode(episode_id: uuid.UUID) -> EpisodeResponse:
    episode = await get_entity(
        episode_id,
        Episode,
        opts=[selectinload(Episode.image_val)]
    )
    return EpisodeResponse(
        **episode.__dict__,
        cover_link=episode.image_val.file_url
    )


@episodes_router.get("/", response_model=Page[EpisodeResponse])
async def list_episode(
        show_id: Optional[uuid.UUID] = None,
        series: Optional[str] = None,
        episode_title: Optional[str] = None
) -> Page[EpisodeResponse]:
    conditions = [(model_field == field_val) for model_field, field_val in [(Episode.show_id, show_id),
                                                                            (Episode.series, series),
                                                                            ] if field_val is not None]
    if episode_title:
        conditions.append(Episode.title.ilike(f"%{episode_title}%"))
    episodes, total, param = await get_entities_paginated(
        Episode,
        conditions,
        opts=[selectinload(Episode.image_val)],
        order_by=lambda: Episode.season_num*10+Episode.episode_num
    )
    episodes = [EpisodeResponse(
        **episode[0].__dict__,
        cover_link=episode[0].image_val.file_url
    ) for episode in episodes]
    return create_page(episodes, total, param)
