import xml.etree.ElementTree as ETree

from episodes.models import Episode
from images.models import Image
from podcast_rss_generator import ImageDTO, generate_show_rss_feed, PodcastOwnerDTO, gen_episode, GUIDDataDTO, el_to_str
from podcast_rss_generator.rss_generator.constants import PODCAST_NAMESPACES
from users import User
from utils.column_factories import datetime_now_no_tz, str_uuid_factory
from utils.constants import GENERATOR_VERSION
from utils.db import save_entity
from utils.files import get_s3_key, upload_file_to_s3, FileKind, fetch_file, remove_file_from_s3, get_s3_key_from_link


async def generate_new_show_feed(image: Image,
                                 show_create_param,
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


async def add_new_episode_to_feed(show, episode: Episode, cover_link_data: str, user_id: str):
    for namespace, url in PODCAST_NAMESPACES:
        ETree.register_namespace(namespace, url)

    rss_content = await fetch_file(show.feed_file_link)
    tree = ETree.ElementTree(ETree.fromstring(rss_content))

    channel = tree.find("channel")
    xml_episode = gen_episode(
        episode.title,
        episode.description,
        episode.episode_link,
        episode.file_link,
        cover_link_data,
        episode_guid=GUIDDataDTO(str_uuid_factory(), False),
        season_num=episode.season_num,
        episode_num=episode.episode_num,
        explicit=episode.explicit,
        duration=episode.duration,
        episode_type=episode.episode_type,
        pub_date=datetime_now_no_tz()
    )
    channel.append(xml_episode)
    updated_rss_content = el_to_str(tree.getroot(), add_xml_header=True)
    show_id = str(show.id)

    await remove_file_from_s3(get_s3_key_from_link(show.feed_file_link))

    rss_file_s3_key = get_s3_key(f"{show_id.replace('-', '')}.xml", show_id.replace('-', ''), user_id)
    show.feed_file_link = await upload_file_to_s3(rss_file_s3_key, updated_rss_content.decode('utf-8'), FileKind.XML)

    await save_entity(show)
    return await upload_file_to_s3(rss_file_s3_key, updated_rss_content.decode('utf-8'), FileKind.XML)
