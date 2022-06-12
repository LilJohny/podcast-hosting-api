import uuid

from fastapi import APIRouter
from fastapi.responses import Response

from shows.models import Show
from utils.db import get_entity
from utils.files import fetch_file

rss_router = APIRouter(prefix="/rss")


@rss_router.head("/{show_id}/feed.xml")
@rss_router.get("/{show_id}/feed.xml")
async def rss_server(show_id: uuid.UUID):
    show = await get_entity(show_id, Show)
    feed_file_content = await fetch_file(show.feed_file_link)
    return Response(feed_file_content.decode("utf-8"), media_type="application/xml")
