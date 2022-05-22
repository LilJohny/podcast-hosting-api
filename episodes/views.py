import uuid
from typing import Optional

from fastapi import APIRouter, status, Depends, UploadFile, File, HTTPException
from fastapi_pagination import Params, paginate, Page

from episodes.models import EpisodeParam, Episode, EpisodeResponse
from settings import get_entity, save_entity, get_entities
from utils.files import get_s3_key, upload_file_to_s3, FileKind
from utils.serializers import serialize
from views import delete_entity, update_entity, read_entity

episodes_router = APIRouter(prefix="/episodes")


@episodes_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_episode(episode_param: EpisodeParam, episode_file: UploadFile = File(...)) -> EpisodeResponse:
    s3_key = get_s3_key(episode_file.filename, episode_param.title)
    episode_link = await upload_file_to_s3(s3_key, episode_file.file, FileKind.AUDIO)
    episode = Episode(**episode_param.dict(), file_link=episode_link, episode_link="", is_removed=False)
    await save_entity(episode)
    return serialize(episode, EpisodeResponse)


@episodes_router.delete("/{episode_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_episode(episode_id: uuid.UUID):
    return await delete_entity(episode_id, Episode)


@episodes_router.put("/{episode_id}", status_code=status.HTTP_200_OK)
async def update_episode(episode_id: uuid.UUID, episode_param: EpisodeParam) -> EpisodeResponse:
    return await update_entity(episode_id, Episode, episode_param, EpisodeResponse)


@episodes_router.get("/{episode_id}")
async def read_episode(episode_id: uuid.UUID) -> EpisodeResponse:
    return await read_entity(episode_id, Episode, EpisodeResponse)


@episodes_router.get("/", response_model=Page[EpisodeResponse])
async def list_episode(show_id: Optional[uuid.UUID] = None,
                       series: Optional[str] = None,
                       episode_title: Optional[str] = None,
                       params: Params = Depends()):
    conditions = [(model_field == field_val) for model_field, field_val in [(Episode.show_id, show_id),
                                                                            (Episode.series, series),
                                                                            (Episode.title, episode_title)
                                                                            ] if field_val is not None]

    episodes = await get_entities(Episode, conditions)
    episodes = serialize(episodes, EpisodeResponse, many=True)
    return paginate(episodes, params)
