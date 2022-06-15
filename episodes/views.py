import os
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, status, UploadFile, File, HTTPException, Depends
from fastapi_pagination import Page, create_page
from sqlalchemy.orm import selectinload

from episodes.models import Episode
from episodes.schemas import EpisodeCreate, EpisodeResponse, EpisodeUpdate, EpisodeFileUploadResponse
from users import User, current_active_user
from utils.audio import DURATION_FINDERS
from utils.db import save_entity, get_entities_paginated, get_entity
from utils.files import upload_file_to_s3, FileKind, get_s3_key
from views import delete_entity, update_entity

episodes_router = APIRouter(prefix="/episodes")


@episodes_router.post("/file/upload", status_code=status.HTTP_201_CREATED, response_model=EpisodeFileUploadResponse)
async def upload_episode_file(
        episode_title: str,
        episode_file: UploadFile = File(...),
        user: User = Depends(current_active_user)
) -> EpisodeFileUploadResponse:
    episode_s3_key = get_s3_key(episode_file.filename, episode_title, user.id)
    episode_link = await upload_file_to_s3(episode_s3_key, episode_file.file,
                                           FileKind.AUDIO)
    _, file_extension = os.path.splitext(episode_file.filename)
    duration_finder = DURATION_FINDERS.get(file_extension)
    if duration_finder is None:
        raise HTTPException(status_code=400, detail="Amphora supports only .mp3 and .wave audio formats")
    episode_duration = duration_finder(episode_file.file)
    return EpisodeFileUploadResponse(
        episode_link=episode_link,
        file_extension=file_extension,
        episode_duration=episode_duration
    )


@episodes_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=EpisodeResponse)
async def create_episode(episode_param: EpisodeCreate) -> EpisodeResponse:

    episode_param_data = episode_param.dict()
    cover_link_data = episode_param_data.pop("cover_link")
    episode = Episode(
        **episode_param_data,
        episode_link=f"/episode_id",
    )
    await save_entity(episode)
    return EpisodeResponse(
        **episode.__dict__,
        cover_link=cover_link_data
    )


@episodes_router.delete("/{episode_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_episode(episode_id: UUID):
    return await delete_entity(episode_id, Episode)


@episodes_router.put("/{episode_id}", status_code=status.HTTP_200_OK, response_model=EpisodeResponse)
async def update_episode(episode_id: UUID, episode_param: EpisodeUpdate) -> EpisodeResponse:
    episode_param_data = {key: episode_param.dict()[key] for key in episode_param.dict() if episode_param.dict()[key]}
    return await update_entity(episode_id, Episode, episode_param_data, EpisodeResponse)


@episodes_router.get("/{episode_id}", response_model=EpisodeResponse)
async def read_episode(episode_id: UUID) -> EpisodeResponse:
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
        show_id: Optional[UUID] = None,
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
        order_by=lambda: Episode.season_num * 10 + Episode.episode_num
    )
    episodes = [EpisodeResponse(
        **episode[0].__dict__,
        cover_link=episode[0].image_val.file_url
    ) for episode in episodes]
    return create_page(episodes, total, param)
