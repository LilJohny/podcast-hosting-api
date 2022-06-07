import enum
import os
from tempfile import SpooledTemporaryFile
from typing import Union

import httpx

from settings import aws_session, BUCKET_NAME, PUBLIC_URL


class FileKind(str, enum.Enum):
    IMAGE = "public/images"
    AUDIO = "public/audios"
    XML = "public/xml"


class FileUploadFailedException(Exception):
    def __init__(self, file_name: str):
        super().__init__(f"Failed to upload file {file_name}!")


def get_s3_key(file_name: str, title: str) -> str:
    _, ext = os.path.splitext(file_name)
    s3_key = "".join([title, ext])
    return s3_key


async def upload_rss_to_s3(blob_s3_key: str, file_data: str):
    async with aws_session.resource("s3") as s3:
        try:
            stored_object = await s3.Object(BUCKET_NAME, blob_s3_key)
            await stored_object.put(Body=file_data)
            return 200
        except Exception as err:
            print(err)
            return 409


async def upload_fileobj_to_s3(blob_s3_key: str, file_data: SpooledTemporaryFile):
    async with aws_session.client("s3") as s3:
        try:
            await s3.upload_fileobj(file_data, BUCKET_NAME, blob_s3_key)
            return 200
        except Exception as err:
            print(err)
            return 409


async def upload_file_to_s3(file_key: str,
                            file_data: Union[SpooledTemporaryFile, str],
                            file_kind: FileKind) -> str:
    blob_s3_key = f"{file_kind.value}/{file_key}"
    response_code = await upload_rss_to_s3(blob_s3_key, file_data) \
        if file_kind == FileKind.XML else await upload_fileobj_to_s3(blob_s3_key, file_data)
    if response_code == 200:
        return f"{PUBLIC_URL}/{blob_s3_key}"
    else:
        raise FileUploadFailedException(blob_s3_key)


async def fetch_file(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
    return resp.content
