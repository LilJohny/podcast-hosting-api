from schemas import UUIDSchema, TitledSchema


class ImageCreate(TitledSchema):
    title: str


class ImageResponse(ImageCreate, UUIDSchema):
    file_url: str
