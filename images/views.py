import uuid

from fastapi import status, APIRouter, UploadFile, File
from fastapi_pagination import Page, create_page

from images.models import Image
from images.schemas import ImageResponse
from utils.db import save_entity, get_entities
from utils.files import upload_file_to_s3, FileKind, get_s3_key
from views import delete_entity, read_entity

images_router = APIRouter(prefix="/images")


@images_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_image(image_title: str, image_file: UploadFile = File(...)) -> ImageResponse:
    image_s3_key = get_s3_key(image_file.filename, image_title)
    image_url = await upload_file_to_s3(image_s3_key, image_file.file.read(), FileKind.IMAGE)
    image = Image(title=image_title, file_url=image_url)
    await save_entity(image)
    return image.__dict__


@images_router.delete("/{image_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_image(image_id: uuid.UUID):
    return await delete_entity(image_id, Image)


@images_router.get("/{image_id}", status_code=status.HTTP_200_OK)
async def read_image(image_id: uuid.UUID) -> ImageResponse:
    image = await read_entity(image_id, Image, ImageResponse)
    return image.__dict__


@images_router.get("/", response_model=Page[ImageResponse])
async def list_images():
    images, total, params = await get_entities(Image)
    images = [ImageResponse(**image[0].__dict__) for image in images]
    return create_page(images, total, params)
