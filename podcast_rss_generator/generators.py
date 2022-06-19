from images.models import Image
from podcast_rss_generator import ImageDTO, generate_show_rss_feed, PodcastOwnerDTO
from shows.schemas import ShowCreate
from users import User
from utils.column_factories import datetime_now_no_tz
from utils.constants import GENERATOR_VERSION
from utils.files import get_s3_key, upload_file_to_s3, FileKind


async def generate_new_show_feed(image: Image,
                                 show_create_param: ShowCreate,
                                 show_link: str,
                                 show_feed_link: str,
                                 show_id: str,
                                 user: User
                                 ) -> str:
    image_dto = ImageDTO(title=image.title, url=image.file_url, height=1400, width=1400, link=image.file_url)
    rss_feed = generate_show_rss_feed(
        show_create_param.title,
        show_feed_link,
        show_link,
        image.file_url,
        show_create_param.description,
        GENERATOR_VERSION,
        show_create_param.language,
        show_create_param.show_copyright,
        datetime_now_no_tz(),
        image_dto,
        PodcastOwnerDTO(name=f"{user.first_name} {user.last_name}", email=user.email)
    )
    rss_file_s3_key = get_s3_key(f"{show_id.replace('-', '')}.xml", show_id.replace('-', ''), user.id)
    rss_file_link = await upload_file_to_s3(rss_file_s3_key, rss_feed.decode('utf-8'), FileKind.XML)
    return rss_file_link
