from typing import List
from uuid import UUID

from fastapi import APIRouter

from series.models import Series
from utils.db import save_entities, get_entities

series_router = APIRouter(prefix="/series")


async def create_series_batch(show_id: str, series_param: List[str]):
    series_arr = [Series(name=series_name, show_id=show_id) for series_name in series_param]
    await save_entities(series_arr)
    return series_arr


@series_router.get("/{show_id}")
async def get_series_by_show_id(show_id: UUID):
    series = await get_entities(
        Series,
        conditions=[Series.show_id == show_id],
        only_columns=[Series.name]
    )
    return series
