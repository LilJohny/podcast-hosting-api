from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from fastapi_pagination import resolve_params
from fastapi_pagination.bases import AbstractParams, AbstractPage
from fastapi_pagination.ext.sqlalchemy import paginate_query
from sqlalchemy import func, select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select




async def paginate(
    session: AsyncSession,
    query: Select,
    params: Optional[AbstractParams] = None,
) -> AbstractPage:  # pragma: no cover # FIXME: fix coverage report generation
    #print(params)
    params = resolve_params(params)

    total = await session.scalar(select(func.count()).select_from(query.subquery()))  # type: ignore
    items = await session.execute(paginate_query(query, params))
    return items.all(), total, params