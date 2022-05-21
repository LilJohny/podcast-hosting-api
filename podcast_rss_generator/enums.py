from enum import Enum


class PodcastType(Enum):
    EPISODIC = "episodic"


class ITunesXML(Enum):
    IMAGE = "itunes:image"
    EXPLICIT = "itunes:explicit"
    AUTHOR = "itunes:author"
    DESCRIPTION = "itunes:description"
    OWNER = "itunes:owner"
    NAME = "itunes:name"
    EMAIL = "itunes:email"
    TYPE = "itunes:type"
    SUMMARY = "itunes:summary"


class EpisodeType(Enum):
    FULL = "full"
