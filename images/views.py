from uuid import UUID

from fastapi import status, APIRouter, UploadFile, File, Depends
from fastapi_pagination import Page, create_page

from images.models import Image
from images.schemas import ImageResponse
from users import User, current_active_user
from utils.db import save_entity, get_entities_paginated, delete_entity_permanent, get_entity
from utils.files import upload_file_to_s3, FileKind, get_s3_key, get_s3_key_from_link, remove_file_from_s3
from views import read_entity

images_router = APIRouter(prefix="/images")


@images_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ImageResponse)
async def create_image(
        image_title: str,
        image_file: UploadFile = File(...),
        user: User = Depends(current_active_user)
) -> ImageResponse:
    image_s3_key = get_s3_key(image_file.filename, image_title, user.id)
    image_url = await upload_file_to_s3(image_s3_key, image_file.file, FileKind.IMAGE)
    image = Image(title=image_title, file_url=image_url)
    await save_entity(image)
    return image.__dict__


@images_router.delete("/{image_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_image(image_id: UUID):
    image_url = await get_entity(image_id, Image, only_columns=[Image.file_url])
    image_s3_key = get_s3_key_from_link(image_url)
    await remove_file_from_s3(image_s3_key)
    return await delete_entity_permanent(image_id, Image)


@images_router.get("/{image_id}", status_code=status.HTTP_200_OK)
async def read_image(image_id: UUID) -> ImageResponse:
    image = await read_entity(image_id, Image)
    return image.__dict__


@images_router.get("/", response_model=Page[ImageResponse])
async def list_images():
    images, total, params = await get_entities_paginated(Image)
    images = [ImageResponse(**image[0].__dict__) for image in images]
    return create_page(images, total, params)
