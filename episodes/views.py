import os
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, status, UploadFile, File, HTTPException, Depends
from fastapi_pagination import Page, create_page
from sqlalchemy.orm import selectinload

from episodes.models import Episode
from episodes.schemas import EpisodeCreate, EpisodeResponse, EpisodeUpdate, EpisodeFileUploadResponse
from podcast_rss_generator.generators import add_new_episode_to_feed
from shows.models import Show
from users import User, current_active_user
from utils.audio import AUDIO_FILE_KINDS, get_duration, decode_webm_to_mp3
from utils.column_factories import str_uuid_factory
from utils.db import save_entity, get_entities, get_entity
from utils.files import upload_file_to_s3, FileKind, get_s3_key
from utils.links import get_episode_link
from views import delete_entity, update_entity

episodes_router = APIRouter(prefix="/episodes")


@episodes_router.post("/file/recorded", status_code=status.HTTP_201_CREATED, response_model=EpisodeFileUploadResponse)
async def process_recorded_file(
        episode_title: str,
        duration: int,
        episode_file: UploadFile = File(...),
        user: User = Depends(current_active_user)
):
    episode_s3_key = get_s3_key(episode_file.filename, episode_title, user.id)
    episode_link = await upload_file_to_s3(
        episode_s3_key.replace(".webm", ".mp3"),
        decode_webm_to_mp3(episode_file.file),
        FileKind.AUDIO
    )
    return EpisodeFileUploadResponse(
        episode_link=episode_link,
        file_extension=".mp3",
        episode_duration=duration
    )


@episodes_router.post("/file/upload", status_code=status.HTTP_201_CREATED, response_model=EpisodeFileUploadResponse)
async def upload_episode_file(
        episode_title: str,
        episode_file: UploadFile = File(...),
        user: User = Depends(current_active_user)
) -> EpisodeFileUploadResponse:
    episode_s3_key = get_s3_key(episode_file.filename, episode_title, user.id)
    episode_link = await upload_file_to_s3(
        episode_s3_key,
        episode_file.file,
        FileKind.AUDIO
    )
    _, file_extension = os.path.splitext(episode_file.filename)
    duration_finder = AUDIO_FILE_KINDS.get(file_extension)
    if duration_finder is None:
        raise HTTPException(status_code=400, detail="Amphora supports only .mp3 and .wave audio formats")
    episode_duration = get_duration(episode_file.file, duration_finder)
    return EpisodeFileUploadResponse(
        episode_link=episode_link,
        file_extension=file_extension,
        episode_duration=episode_duration
    )


@episodes_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=EpisodeResponse)
async def create_episode(episode_param: EpisodeCreate, user: User = Depends(current_active_user)) -> EpisodeResponse:
    episode_param_data = episode_param.dict()
    cover_link_data = episode_param_data.pop("cover_link")
    episode_id = str_uuid_factory()
    new_episode_link = get_episode_link(episode_param.show_id, episode_id)
    episode = Episode(
        id=episode_id,
        **episode_param_data,
        episode_link=new_episode_link,
    )
    await save_entity(episode)
    show = await get_entity(episode.show_id, Show)
    await add_new_episode_to_feed(show, episode, cover_link_data, user.id)
    return EpisodeResponse(
        **episode.__dict__,
        cover_link=cover_link_data
    )


@episodes_router.delete("/{episode_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_episode(episode_id: UUID, user: User = Depends(current_active_user)):
    return await delete_entity(episode_id, Episode)


@episodes_router.put("/{episode_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_episode(
        episode_id: UUID,
        episode_param: EpisodeUpdate,
        user: User = Depends(current_active_user)
) -> int:
    episode_param_data = episode_param.dict()
    episode_param_data = {key: episode_param_data[key] for key in episode_param_data if episode_param_data[key]}
    await update_entity(episode_id, Episode, episode_param_data)
    return status.HTTP_202_ACCEPTED


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
        episode_title: Optional[str] = None,
        user: User = Depends(current_active_user)
) -> Page[EpisodeResponse]:
    conditions = [(model_field == field_val) for model_field, field_val in [(Episode.show_id, show_id),
                                                                            (Episode.series, series),
                                                                            ] if field_val is not None]
    if episode_title:
        conditions.append(Episode.title.ilike(f"%{episode_title}%"))
    episodes, total, param = await get_entities(
        Episode,
        conditions,
        opts=[selectinload(Episode.image_val)],
        order_by=lambda: Episode.season_num * 10 + Episode.episode_num,
        pagination=True
    )
    episodes = [EpisodeResponse(
        **episode[0].__dict__,
        cover_link=episode[0].image_val.file_url
    ) for episode in episodes]
    return create_page(episodes, total, param)
