import datetime

from podcast_rss_generator.enums import PodcastType, EpisodeType
from podcast_rss_generator.rss_generator import generate_rss, gen_image, PODCAST_ATTRS, XML_LANG, gen_itunes_image, \
    gen_itunes_explicit, gen_itunes_author, gen_atom_link, gen_itunes_summary, gen_podcast_locked, gen_itunes_type, \
    gen_itunes_owner, gen_episode
from podcast_rss_generator.rss_generator.helpers import el_to_str, cdata_wrap, datetime_to_str
from podcast_rss_generator.rss_generator.types import ImageDTO, PodcastOwnerDTO, GUIDDataDTO


def generate_show_rss_feed(show_title: str,
                           self_link: str,
                           podcast_link: str,
                           media_link: str,
                           show_description: str,
                           generator: str,
                           language: str,
                           copyright_: str,
                           last_build_date: datetime.datetime,
                           image: ImageDTO,
                           podcast_owner: PodcastOwnerDTO,
                           podcast_type: PodcastType = PodcastType.EPISODIC,
                           is_explicit=False,
                           is_locked=False,
                           rss_items=None):
    last_build_date_str = datetime_to_str(last_build_date)

    el = generate_rss(title=show_title,
                      podcast_link=podcast_link,
                      media_link=media_link,
                      category="Arts",
                      description=show_description,
                      generator=generator,
                      language=language,
                      copyright=copyright_,
                      lastBuildDate=last_build_date_str,
                      image=image,
                      podcast_owner=podcast_owner,
                      podcast_type=podcast_type,
                      is_explicit=is_explicit,
                      is_locked=is_locked,
                      self_link=self_link,
                      items=rss_items)

    for attr, value in PODCAST_ATTRS.items():
        el.set(attr, value)
    el.set(XML_LANG, "en")

    return el_to_str(el, add_xml_header=True)
