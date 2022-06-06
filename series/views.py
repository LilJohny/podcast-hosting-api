from typing import List

from series.models import Series
from utils.db import save_entities


async def create_series_batch(show_id: str, series_param: List[str]):
    series_arr = [Series(name=series_name, show_id=show_id) for series_name in series_param]
    await save_entities(series_arr)
    return series_arr
