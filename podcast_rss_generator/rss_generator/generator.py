import dataclasses
import datetime
import functools
from typing import Optional, Iterable, Union, Generator

from .constants import MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT
from .elements import DEFAULT_ETREE, GUIDElement, EnclosureElement, ItemElement, CloudElement, CategoryElement, \
    SourceElement, TextInputElement, ImageElement, ItunesImageElement, ItunesExplicitElement, ItunesAuthorElement, \
    AtomLinkElement, ItunesSummaryElement, PodcastLockedElement, ItunesOwnerElement, ItunesTypeElement, LinkElement, \
    ItunesCategoryElement
from .helpers import datetime_to_str, cdata_wrap, to_xml_bool, to_xml_bool_word, p_tag_wrap
from .types import GUIDDataDTO, PodcastOwnerDTO, ImageDTO
from ..enums import ITunesXML, EpisodeType, PodcastType


def add_subelement_with_text(
        root: DEFAULT_ETREE.Element, child_tag: str, text: str, etree=DEFAULT_ETREE
) -> DEFAULT_ETREE.SubElement:
    sub = etree.SubElement(root, child_tag)
    sub.text = text

    return sub


def gen_itunes_image(url: str, etree=DEFAULT_ETREE) -> ItunesImageElement:
    el = etree.Element(ITunesXML.IMAGE.value)
    el.set("href", url)
    return ItunesImageElement(el)


def gen_itunes_explicit(is_explicit: bool = False, etree=DEFAULT_ETREE) -> ItunesExplicitElement:
    el_text = to_xml_bool_word(is_explicit)
    el = etree.Element(ITunesXML.EXPLICIT.value)
    el.text = el_text
    return ItunesExplicitElement(el)


def gen_itunes_author(author_name: str, etree=DEFAULT_ETREE) -> ItunesAuthorElement:
    el = etree.Element(ITunesXML.AUTHOR.value)
    el.text = author_name
    return ItunesAuthorElement(el)


def gen_atom_link(href: str, rel: str, type_: Optional[str] = None, etree=DEFAULT_ETREE) -> AtomLinkElement:
    el = etree.Element("atom:link")
    el.set("href", href)
    el.set("rel", rel)
    if type_:
        el.set("type", type_)
    return AtomLinkElement(el)


def gen_itunes_summary(description: str, etree=DEFAULT_ETREE) -> ItunesSummaryElement:
    el = etree.Element(ITunesXML.SUMMARY.value)
    el.text = description
    return ItunesSummaryElement(el)


def gen_podcast_locked(owner_email: str, is_locked: bool = False, etree=DEFAULT_ETREE) -> PodcastLockedElement:
    el_text = to_xml_bool_word(is_locked).capitalize()
    el = etree.Element("podcast:locked", owner=owner_email)
    el.text = el_text
    return PodcastLockedElement(el)


def gen_itunes_owner(owner_name: str, owner_email: str, etree=DEFAULT_ETREE) -> ItunesOwnerElement:
    el = etree.Element(ITunesXML.OWNER.value)
    add_subelement_with_text_etree = functools.partial(
        add_subelement_with_text, etree=etree
    )

    add_subelement_with_text_etree(el, ITunesXML.NAME.value, owner_name)
    add_subelement_with_text_etree(el, ITunesXML.EMAIL.value, owner_email)
    return ItunesOwnerElement(el)


def gen_itunes_type(podcasting_type: str, etree=DEFAULT_ETREE) -> ItunesTypeElement:
    el = etree.Element(ITunesXML.TYPE.value)
    el.text = podcasting_type
    return ItunesTypeElement(el)


def gen_image(
        url: str,
        title: str,
        link: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        etree=DEFAULT_ETREE,
) -> ImageElement:
    image = etree.Element("image")

    add_subelement_with_text_etree = functools.partial(
        add_subelement_with_text, etree=etree
    )

    add_subelement_with_text_etree(image, "url", url)
    add_subelement_with_text_etree(image, "title", title)
    add_subelement_with_text_etree(image, "link", link)

    if width is not None:
        if width > MAX_IMAGE_WIDTH:
            raise ValueError(f"Max width is {MAX_IMAGE_WIDTH}")

        add_subelement_with_text_etree(image, "width", str(width))

    if height is not None:
        if width > MAX_IMAGE_HEIGHT:
            raise ValueError(f"Max height is {MAX_IMAGE_HEIGHT}")

        add_subelement_with_text_etree(image, "height", str(height))

    return ImageElement(image)


def gen_cloud(
        domain: str,
        port: int,
        path: str,
        registerProcedure: str,
        protocol: str,
        etree=DEFAULT_ETREE,
) -> CloudElement:
    return CloudElement(
        etree.Element(
            "cloud",
            domain=domain,
            port=str(port),
            path=path,
            registerProcedure=registerProcedure,
            protocol=protocol,
        )
    )


def gen_text_input(title: str, description: str, name: str, link: str, etree=DEFAULT_ETREE) -> TextInputElement:
    text_input = etree.Element("textInput")

    add_subelement_with_text_etree = functools.partial(
        add_subelement_with_text, etree=etree
    )

    add_subelement_with_text_etree(text_input, "title", title)
    add_subelement_with_text_etree(text_input, "description", description)
    add_subelement_with_text_etree(text_input, "name", name)
    add_subelement_with_text_etree(text_input, "link", link)

    return TextInputElement(text_input)


def gen_category(category: str, domain: Optional[str] = None, etree=DEFAULT_ETREE) -> CategoryElement:
    element = etree.Element("category")

    if domain is not None:
        element.attrib["domain"] = domain

    element.text = category

    return CategoryElement(element)


def not_none(
        *elements: Iterable[Optional[DEFAULT_ETREE.Element]],
) -> Generator[DEFAULT_ETREE.Element, None, None]:
    return (e for e in elements if e is not None)


def validate_either(*args, msg=None) -> None:
    if not any(arg is not None for arg in args):
        raise ValueError(msg)


def gen_item(
        title: Optional[str] = None,
        link: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
        category: Union[Optional[str], Iterable[CategoryElement]] = None,
        comments: Optional[str] = None,
        enclosure: Optional[EnclosureElement] = None,
        guid: Optional[GUIDElement] = None,
        pubDate: Optional[str] = None,
        source: Optional[SourceElement] = None,
        etree=DEFAULT_ETREE,
) -> ItemElement:
    validate_either(
        title, description, msg="Either title or description must be set."
    )

    args = {k: v for k, v in locals().items() if v is not None}

    # Remove elements that we are handling specifically.
    args.pop("etree", None)

    item = etree.Element("item")

    # Category can be a string or CategoryElements, handle the latter case.
    # TODO: Collapse into 'add complex elements'
    if category is not None and type(category) is not str:
        item.extend(category)
        args.pop("category")

    # Add complex elements.
    item.extend(
        list(
            not_none(
                args.pop("enclosure", None),
                args.pop("guid", None),
                args.pop("source", None),
            )
        )
    )

    add_subelement_with_text_etree = functools.partial(
        add_subelement_with_text, etree=etree
    )

    for tag_name, tag_value in args.items():
        add_subelement_with_text_etree(item, tag_name, tag_value)

    return ItemElement(item)


def gen_guid(guid: str, isPermaLink: bool = True, etree=DEFAULT_ETREE) -> GUIDElement:
    el = etree.Element("guid", isPermaLink=to_xml_bool(isPermaLink))
    el.text = guid
    return GUIDElement(el)


def gen_link(link: str, etree=DEFAULT_ETREE) -> LinkElement:
    el = etree.Element("link")
    el.text = link
    return LinkElement(el)


def gen_itunes_category(category: str, subcategory: Optional[str] = None, etree=DEFAULT_ETREE) -> ItunesCategoryElement:
    el = etree.Element("itunes:category", text=category)
    if subcategory:
        sub_el = etree.Element("itunes:category", text=subcategory)
        el.append(sub_el)
    return ItunesCategoryElement(el)


def gen_enclosure(url: str, length: int, enc_type: str, etree=DEFAULT_ETREE) -> EnclosureElement:
    return EnclosureElement(
        etree.Element("enclosure", url=url, length=str(length), type=enc_type)
    )


def gen_source(text: str, url: str, etree=DEFAULT_ETREE) -> SourceElement:
    source = etree.Element("source", url=url)
    source.text = text

    return SourceElement(source)


def generate_rss(
        title: str,
        podcast_link: str,
        media_link: str,
        description: str,
        language: Optional[str],
        copyright: Optional[str],
        lastBuildDate: Optional[str],
        category: Optional[str],
        generator: Optional[str],
        image: Optional[ImageDTO],
        podcast_owner: PodcastOwnerDTO,
        podcast_type: PodcastType = PodcastType.EPISODIC,
        is_explicit=False,
        is_locked=False,
        items: Optional[Iterable[ItemElement]] = None,
        etree=DEFAULT_ETREE,
) -> DEFAULT_ETREE.Element:
    args = {k: v for k, v in locals().items() if v is not None}

    # Remove elements that we are handling specifically.

    rss = etree.Element("rss", version="2.0")
    channel = etree.SubElement(rss, "channel")

    # Add required subelements.
    add_subelement_with_text_etree = functools.partial(
        add_subelement_with_text, etree=etree
    )
    podcast_link = gen_link(podcast_link)
    itunes_image = gen_itunes_image(image.url)
    itunes_summary = gen_itunes_summary(description)
    podcast_locked = gen_podcast_locked(podcast_owner.email, is_locked)
    itunes_author = gen_itunes_author(podcast_owner.name)
    itunes_owner = gen_itunes_owner(podcast_owner.name, podcast_owner.email)
    explicit = gen_itunes_explicit(is_explicit)
    itunes_type = gen_itunes_type(podcast_type.value)
    self_atom_link = gen_atom_link(href=f"{media_link}/feed.xml", rel="self", type_="application/rss+xml")
    itunes_category = gen_itunes_category("Arts", "Books")
    image_el = gen_image(**dataclasses.asdict(image))
    order_elements_to_add = [
        "title",
        ("link", podcast_link),
        ("self_atom_link", self_atom_link),
        "description",
        "generator",
        "lastBuildDate",
        "language",
        "copyright",
        ("itunes:image", itunes_image),
        ("image", image_el),
        ("itunes:summary", itunes_summary),
        ("podcast:locked", podcast_locked),
        ("itunes:author", itunes_author),
        ("itunes:owner", itunes_owner),
        ("itunes:explicit", explicit),
        ("itunes:type", itunes_type),
        ("itunes:category", itunes_category)
    ]
    for element in order_elements_to_add:
        if isinstance(element, str):
            val = args.get(element)
            add_subelement_with_text_etree(channel, element, val)
        else:
            val = element[1]
            channel.append(val)

    keys_to_pop = ["etree", "items", "title", "link", "description", "image", "podcast_link", "media_link",
                   "podcast_owner", "podcast_type", "is_explicit", "is_locked", "language", "copyright",
                   "lastBuildDate", "category", "generator"]
    for pop_key in keys_to_pop:
        args.pop(pop_key, None)
    # Add any other optional fields that were passed as subelements.
    for title, value in args.items():
        add_subelement_with_text_etree(channel, title, value)

    if items is not None:
        channel.extend(items)

    return rss


def gen_episode(
        episode_title: str,
        description: str,
        episode_link: str,
        file_link: str,
        cover_image_link: str,
        episode_guid: GUIDDataDTO,
        episode_num: int,
        season_num: int,
        explicit: bool,
        pub_date: datetime.datetime,
        duration: int,
        episode_type: EpisodeType,
        etree=DEFAULT_ETREE
):
    pub_date = datetime_to_str(pub_date)
    duration = str(duration)
    season_num = str(season_num)
    episode_num = str(episode_num)
    episode_title_cdata = cdata_wrap(episode_title)
    item = etree.Element("item")
    add_subelement_with_text_etree = functools.partial(
        add_subelement_with_text, etree=etree
    )
    args = [('title', episode_title_cdata),
            ('itunes:title', episode_title_cdata),
            ('itunes:summary', description),
            ('description', cdata_wrap(p_tag_wrap(description))),
            ('link', episode_link),
            ('enclosure', gen_enclosure(file_link, 8153337, "audio/mpeg")),
            ('guid', gen_guid(episode_guid.url, episode_guid.isPermalink)),
            ('itunes:image', gen_itunes_image(cover_image_link)),
            ('itunes:duration', duration),
            ('itunes:episodeType', episode_type.value),
            ('itunes:episode', episode_num),
            ('itunes:season', season_num),
            ('itunes:explicit', to_xml_bool_word(explicit)),
            ('pubDate', pub_date)]

    for key, value in args:
        if isinstance(value, str) or isinstance(value, int):
            add_subelement_with_text_etree(item, key, value)
        else:
            item.append(value)

    return item
