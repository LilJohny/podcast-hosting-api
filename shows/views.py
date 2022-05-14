import uuid
from fastapi import status, APIRouter

shows_router = APIRouter(prefix="/shows")


@shows_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_show():
    pass


@shows_router.delete("/{show_id}")
def delete_show(show_id: uuid.UUID):
    pass


@shows_router.put("/{show_id}")
def update_show(show_id: uuid.UUID):
    pass


@shows_router.get("/{show_id}")
def read_show(show_id: uuid.UUID):
    pass


@shows_router.get("/")
def list_show():
    pass
