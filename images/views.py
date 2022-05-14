import uuid
from fastapi import status, APIRouter
from images.models import ImageBase, Image
from db import save_entity, get_entity

images_router = APIRouter(prefix="/images")


@images_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_image(image_param: ImageBase):
    image = Image(**image_param.dict(), is_removed=False, id=str(uuid.uuid4()))
    await save_entity(image)
    return status.HTTP_201_CREATED


@images_router.delete("/{image_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_image(image_id: str):
    image = await get_entity(image_id, Image)
    image.is_removed = True
    await save_entity(image)
    return status.HTTP_202_ACCEPTED


@images_router.put("/{image_id}")
def update_image(image_id: uuid.UUID, image_param: ImageBase):
    pass


@images_router.get("/{image_id}", status_code=status.HTTP_200_OK)
async def read_image(image_id: str) -> ImageBase:
    image = await get_entity(image_id, Image)
    return ImageBase(**image.dict())


@images_router.get("/")
def list_image():
    pass
