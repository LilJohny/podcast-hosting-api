import uuid
from typing import Optional

from fastapi import APIRouter, status, Depends, UploadFile, File
from fastapi_pagination import Params, paginate, Page

from episodes.models import EpisodeParam, Episode
from file_utils import upload_file_to_s3, FileKind, get_s3_key
from settings import get_entity, save_entity, get_entities

episodes_router = APIRouter(prefix="/episodes")


@episodes_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_episode(episode_param: EpisodeParam, episode_file: UploadFile = File(...)) -> Episode:
    s3_key = get_s3_key(episode_file.filename, episode_param.title)
    episode_link = await upload_file_to_s3(s3_key, episode_file.file, FileKind.AUDIO)
    episode = Episode(**episode_param.dict(), file_link=episode_link, episode_link="", is_removed=False)
    await save_entity(episode)
    return episode


@episodes_router.delete("/{episode_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_episode(episode_id: str):
    episode = await get_entity(episode_id, Episode)
    episode.is_removed = True
    await save_entity(episode)
    return status.HTTP_202_ACCEPTED


@episodes_router.put("/{episode_id}", status_code=status.HTTP_200_OK)
async def update_episode(episode_id: str, episode_param: EpisodeParam) -> Episode:
    episode = await get_entity(episode_id, Episode)
    episode_data = episode.dict()
    episode_data.update(episode_param.dict())
    episode = Episode(**episode_data)
    await save_entity(episode)
    return episode


@episodes_router.get("/{episode_id}")
async def read_episode(episode_id: str) -> EpisodeParam:
    image = await get_entity(episode_id, Episode)
    return EpisodeParam(**image.dict())


@episodes_router.get("/", response_model=Page[Episode])
async def list_episode(show_id: Optional[uuid.UUID] = None,
                       series: Optional[str] = None,
                       episode_title: Optional[str] = None,
                       params: Params = Depends()):
    conditions = [(model_field == field_val) for model_field, field_val in [(Episode.show_id, show_id),
                                                                            (Episode.series, series),
                                                                            (Episode.title, episode_title)]]

    episodes = await get_entities(Episode, conditions)
    return paginate(episodes, params)
