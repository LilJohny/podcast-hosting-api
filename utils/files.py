import enum
import os

import httpx

from settings import aws_session, BUCKET_NAME, PUBLIC_URL


class FileKind(enum.Enum):
    IMAGE = "public/images"
    AUDIO = "public/audios"
    XML = "public/xml"


def get_s3_key(file_name: str, title: str) -> str:
    _, ext = os.path.splitext(file_name)
    s3_key = "".join([title, ext])
    return s3_key


async def upload_file_to_s3(file_key: str, file_data, file_kind: FileKind) -> str:
    blob_s3_key = f"{file_kind.value}/{file_key}"
    async with aws_session.resource("s3") as s3:
        try:
            stored_object = await s3.Object(BUCKET_NAME, blob_s3_key)
            await stored_object.put(Body=file_data)
        except Exception as err:
            print(err)
    return f"{PUBLIC_URL}/{blob_s3_key}"


async def fetch_file(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
    return resp.content
