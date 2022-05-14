import uuid
from fastapi import status, APIRouter
from images.models import ImageBase, Image
from db import save_entity

images_router = APIRouter(prefix="/images")


@images_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_show(image_param: ImageBase):
    image = Image(**image_param.dict(), is_removed=False)
    await save_entity(image)
    return status.HTTP_201_CREATED


@images_router.delete("/{image_id}")
def delete_show(image_id: uuid.UUID):
    pass


@images_router.put("/{image_id}")
def update_show(image_id: uuid.UUID):
    pass


@images_router.get("/{image_id}")
def read_show(image_id: uuid.UUID):
    pass


@images_router.get("/")
def list_show():
    pass
