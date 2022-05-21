import uuid

from fastapi import status, APIRouter, Depends, UploadFile, File, HTTPException
from fastapi_pagination import paginate, Page, Params

from file_utils import upload_file_to_s3, FileKind, get_s3_key
from images.models import Image, ImageResponse
from settings import save_entity, get_entity, get_entities
from utils import serialize

images_router = APIRouter(prefix="/images")


@images_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_image(image_title: str, image_file: UploadFile = File(...)) -> ImageResponse:
    s3_key = get_s3_key(image_file.filename, image_title)
    image_url = await upload_file_to_s3(s3_key, image_file.file, FileKind.IMAGE)
    image = Image(title=image_title, file_url=image_url, is_removed=False)
    await save_entity(image)
    return serialize(image, ImageResponse)


@images_router.delete("/{image_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_image(image_id: uuid.UUID):
    image = await get_entity(str(image_id), Image)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    image.is_removed = True
    await save_entity(image)
    return status.HTTP_202_ACCEPTED


@images_router.get("/{image_id}", status_code=status.HTTP_200_OK)
async def read_image(image_id: uuid.UUID) -> ImageResponse:
    image = await get_entity(str(image_id), Image)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return serialize(image, ImageResponse)



@images_router.get("/", response_model=Page[ImageResponse])
async def list_images(params: Params = Depends()):
    images = await get_entities(Image)
    images = serialize(images, ImageResponse, many=True)
    return paginate(images, params)
