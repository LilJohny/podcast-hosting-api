import enum

from settings import aws_session, bucket_name, public_url


class FileKind(enum.Enum):
    IMAGE = "public/images"
    AUDIO = "public/audios"


async def upload_file_to_s3(file_name, file_data, file_kind: FileKind):
    blob_s3_key = f"{file_kind.value}/{file_name}"
    async with aws_session.client("s3") as s3:
        try:
            a = await s3.upload_fileobj(file_data, bucket_name, blob_s3_key)
            print(a)
        except Exception as err:
            print(err)
    return f"{public_url}/{blob_s3_key}"
