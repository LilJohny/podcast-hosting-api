import datetime

from .enums import PodcastType, EpisodeType
from .rss_generator import generate_rss, gen_image, PODCAST_ATTRS, XML_LANG, gen_itunes_image, gen_itunes_explicit, \
    gen_itunes_author, gen_atom_link, gen_itunes_summary, gen_podcast_locked, gen_itunes_type, gen_itunes_owner, \
    gen_episode
from .rss_generator.helpers import el_to_str, cdata_wrap, datetime_to_str
from .rss_generator.types import ImageDTO, PodcastOwnerDTO, GUIDDataDTO

RSS_FILENAME = "current.xml"


def generate_new_show_rss_feed(show_title: str,
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
    ep = gen_episode("Test episode title",
                     "Test episode description",
                     "https://rss.com/podcasts/testpodcasting/475976",
                     "https://media.rss.com/testpodcasting/20220504_040519_89a86b81ff448fff9303b41c2f249c08.mp3",
                     "https://media.rss.com/testpodcasting/20220504_040548_0072f1134aae6c3a898059c08998ba9b.jpg",
                     episode_guid=GUIDDataDTO("847fa074-cc18-408f-a83b-47f0e0cb394e", False),
                     season_num=1,
                     episode_num=1,
                     explicit=True,
                     duration=204,
                     episode_type=EpisodeType.FULL,
                     pub_date=datetime.datetime.today())

    rss_items = [ ep]

    last_build_date_str = datetime_to_str(last_build_date)
    show_title = cdata_wrap(show_title)
    show_description = cdata_wrap(show_description)
    copyright_ = cdata_wrap(copyright_)
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
                      items=rss_items)

    for attr, value in PODCAST_ATTRS.items():
        el.set(attr, value)
    el.set(XML_LANG, "en")
    with open(RSS_FILENAME, "wb") as f:
        f.write(el_to_str(el, add_xml_header=True))


if __name__ == '__main__':
    generate_new_show_rss_feed(
        show_title="Test podcast",
        podcast_link='https://rss.com/podcasts/testpodcasting',
        media_link="https://media.rss.com/testpodcasting",
        show_description="Test podcast description",
        generator="RSS.com v1.5.6",
        language="en",
        copyright_="Test 2022",
        last_build_date=datetime.datetime.today(),
        image=ImageDTO(
            url="https://media.rss.com/testpodcasting/20220430_080454_9918224fc00636a22c6e36616b92f36c.jpg",
            title="Test podcast",
            link="https://rss.com/podcasts/testpodcasting"
        ),
        podcast_owner=PodcastOwnerDTO(name="Test test", email="little.johny@hotmail.com"),
        is_locked=True
    )
