import datetime
import xml

import pytz


def cdata_wrap(text: str) -> str:
    return fr"<![CDATA[{text}]]>"

def p_tag_wrap(text:str) -> str:
    return f"<p>{text}</p>"

def datetime_to_str(date: datetime.datetime) -> str:
    return date.astimezone(tz=pytz.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")


def el_to_str(rss_xml_element, add_xml_header=False):
    return xml.etree.ElementTree.tostring(rss_xml_element,
                                          encoding='utf8') if add_xml_header else xml.etree.ElementTree.tostring(
        rss_xml_element)


def to_xml_bool(val: bool)->str:
    return "true" if val else "false"

def to_xml_bool_word(val:bool)->str:
    return "yes" if val else "no"
