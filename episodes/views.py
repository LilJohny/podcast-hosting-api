import uuid

from fastapi import APIRouter, status

from db import get_entity, save_entity
from episodes.models import EpisodeDTO, Episode

episodes_router = APIRouter(prefix="/episodes")


@episodes_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_episode(episode_param: EpisodeDTO) -> Episode:
    episode = Episode(**episode_param.dict(), is_removed=False, id=str(uuid.uuid4()))
    await save_entity(episode)
    return episode


@episodes_router.delete("/{episode_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_episode(episode_id: str):
    episode = await get_entity(episode_id, Episode)
    episode.is_removed = True
    await save_entity(episode)
    return status.HTTP_202_ACCEPTED


@episodes_router.put("/{episode_id}", status_code=status.HTTP_200_OK)
async def update_episode(episode_id: str, episode_param: EpisodeDTO) -> Episode:
    episode = await get_entity(episode_id, Episode)
    episode_data = episode.dict()
    episode_data.update(episode_param.dict())
    episode = Episode(**episode_data)
    await save_entity(episode)
    return episode


@episodes_router.get("/{episode_id}")
async def read_episode(episode_id: str) -> EpisodeDTO:
    image = await get_entity(episode_id, Episode)
    return EpisodeDTO(**image.dict())


@episodes_router.get("/")
def list_episode():
    pass
