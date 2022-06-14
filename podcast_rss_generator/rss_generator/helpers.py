import datetime
import xml

import pytz

from podcast_rss_generator.rss_generator.constants import XSLT_STYLE_ELEMENT, UTF_8, UNICODE, DATETIME_GMT_FORMAT, \
    XML_TAG_END, XML_TRUE, XML_FALSE, XML_YES, XML_NO, NEWLINE


def cdata_wrap(text: str) -> str:
    return f"<![CDATA[{text}]]>"


def p_tag_wrap(text: str) -> str:
    return f"<p>{text}</p>"


def datetime_to_str(date: datetime.datetime) -> str:
    return date.astimezone(tz=pytz.UTC).strftime(DATETIME_GMT_FORMAT)


def el_to_str(rss_xml_element, add_xml_header=False) -> bytes:
    if add_xml_header:
        el_lines = xml.etree.ElementTree.tostring(
            rss_xml_element,
            encoding=UNICODE,
            xml_declaration=True
        ).split(XML_TAG_END)
        el_lines[0] += XML_TAG_END
        el_lines.insert(1, XSLT_STYLE_ELEMENT)
        el_str = NEWLINE.join(el_lines).encode(UTF_8)
    else:
        el_str = xml.etree.ElementTree.tostring(rss_xml_element)
    return el_str


def to_xml_bool(val: bool) -> str:
    return XML_TRUE if val else XML_FALSE


def to_xml_bool_word(val: bool) -> str:
    return XML_YES if val else XML_NO
