import enum
import os

from settings import aws_session, BUCKET_NAME, PUBLIC_URL


class FileKind(enum.Enum):
    IMAGE = "public/images"
    AUDIO = "public/audios"


def get_s3_key(file_name: str, title: str) -> str:
    _, ext = os.path.splitext(file_name)
    s3_key = "".join([title, ext])
    return s3_key


async def upload_file_to_s3(file_name: str, file_title: str, file_data, file_kind: FileKind) -> str:
    file_key = get_s3_key(file_name, file_title)
    blob_s3_key = f"{file_kind.value}/{file_key}"
    async with aws_session.client("s3") as s3:
        try:
            response = await s3.upload_fileobj(file_data, BUCKET_NAME, blob_s3_key)
            print(response)
        except Exception as err:
            print(err)
    return f"{PUBLIC_URL}/{blob_s3_key}"
