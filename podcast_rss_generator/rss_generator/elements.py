import xml.etree.ElementTree
from typing import NewType

COMPLEX_ELEMENTS = ["cloud", "textInput", "image"]
DEFAULT_ETREE = xml.etree.ElementTree

ImageElement = NewType("ImageElement", DEFAULT_ETREE.Element)
CloudElement = NewType("CloudElement", DEFAULT_ETREE.Element)
TextInputElement = NewType("TextInputElement", DEFAULT_ETREE.Element)
ItemElement = NewType("ItemElement", DEFAULT_ETREE.Element)
EnclosureElement = NewType("EnclosureElement", DEFAULT_ETREE.Element)
GUIDElement = NewType("GUIDElement", DEFAULT_ETREE.Element)
LinkElement = NewType("LinkElement", DEFAULT_ETREE.Element)
SourceElement = NewType("SourceElement", DEFAULT_ETREE.Element)
CategoryElement = NewType("CategoryElement", DEFAULT_ETREE.Element)
ItunesImageElement = NewType("ItunesImageElement", DEFAULT_ETREE.Element)
ItunesExplicitElement = NewType("ItunesExplicitElement", DEFAULT_ETREE.Element)
ItunesAuthorElement = NewType("ItunesAuthorElement", DEFAULT_ETREE.Element)
ItunesSummaryElement = NewType("ItunesSummaryElement", DEFAULT_ETREE.Element)
ItunesOwnerElement = NewType("ItunesOwnerElement", DEFAULT_ETREE.Element)
ItunesTypeElement = NewType("ItunesTypeElement", DEFAULT_ETREE.Element)
ItunesCategoryElement = NewType("ItunesCategoryElement", DEFAULT_ETREE.Element)
AtomLinkElement = NewType("AtomLinkElement", DEFAULT_ETREE.Element)
PodcastLockedElement = NewType("PodcastLockedElement", DEFAULT_ETREE.Element)