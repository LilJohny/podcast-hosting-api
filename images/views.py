import uuid

from fastapi import status, APIRouter, Depends
from fastapi_pagination import paginate, Page, add_pagination, Params

from db import save_entity, get_entity, get_entities
from images.models import ImageDTO, Image

images_router = APIRouter(prefix="/images")


@images_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_image(image_param: ImageDTO) -> Image:
    image = Image(**image_param.dict(), is_removed=False)
    await save_entity(image)
    return image


@images_router.delete("/{image_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_image(image_id: str):
    image = await get_entity(image_id, Image)
    image.is_removed = True
    await save_entity(image)
    return status.HTTP_202_ACCEPTED


@images_router.get("/{image_id}", status_code=status.HTTP_200_OK)
async def read_image(image_id: uuid.UUID) -> ImageDTO:
    image = await get_entity(str(image_id), Image)
    return ImageDTO(**image.dict())


@images_router.get("/", response_model=Page[Image])
async def list_images(params: Params = Depends()):
    images = await get_entities(Image)
    return paginate(images, params)
