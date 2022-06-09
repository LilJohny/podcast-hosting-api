import datetime
import xml

import pytz

from podcast_rss_generator.rss_generator.constants import xslt_style_element, UTF_8


def cdata_wrap(text: str) -> str:
    return fr"<![CDATA[{text}]]>"


def p_tag_wrap(text: str) -> str:
    return f"<p>{text}</p>"


def datetime_to_str(date: datetime.datetime) -> str:
    return date.astimezone(tz=pytz.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")


def el_to_str(rss_xml_element, add_xml_header=False):
    if add_xml_header:
        el_str = xml.etree.ElementTree.tostring(rss_xml_element, encoding=UTF_8)
        el_lines = el_str.decode(UTF_8).split("\n")
        el_lines.insert(1, xslt_style_element)
        el_str = "\n".join(el_lines).encode(UTF_8)
    else:
        el_str = xml.etree.ElementTree.tostring(rss_xml_element)
    return el_str


def to_xml_bool(val: bool) -> str:
    return "true" if val else "false"


def to_xml_bool_word(val: bool) -> str:
    return "yes" if val else "no"
