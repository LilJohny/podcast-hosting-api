import uuid
from typing import Optional

from deta import Deta
from fastapi import APIRouter, status, Depends
from fastapi_pagination import Params, paginate, Page

from settings import get_entity, save_entity, get_entities
from episodes.models import EpisodeDTO, Episode

episodes_router = APIRouter(prefix="/episodes")

deta = Deta(project_key="a07qpkhz_b5Qn6LCt76CJM9r7tYqcwimtHoM8zEqg", project_id="a07qpkhz")
images_drive = deta.Drive("images")

@episodes_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_episode(episode_param: EpisodeDTO) -> Episode:
    episode = Episode(**episode_param.dict(), is_removed=False)
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
