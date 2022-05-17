import uuid

from deta import Deta
from fastapi import status, APIRouter, Depends, UploadFile, File
from fastapi_pagination import paginate, Page, Params

from db import save_entity, get_entity, get_entities
from images.models import ImageDTO, Image

images_router = APIRouter(prefix="/images")

deta = Deta(project_key="a07qpkhz_b5Qn6LCt76CJM9r7tYqcwimtHoM8zEqg", project_id="a07qpkhz")
images_drive = deta.Drive("images")

@images_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_image(image_title:str, image_file: UploadFile = File(...)) -> Image:
    path = image_file.filename
    image_url = images_drive.put(path, image_file.file)
    image = Image(title=image_title, file_url=f"https://a", is_removed=False)
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
