import enum
from typing import List

STREAMING_OPTIONS = [
    "apple-podcasts",
    "google-podcasts",
    "pocket-casts",
    "soundcloud",
    "spotify",
    "youtube"
]


class StreamingOptionsCoding(enum.Enum):
    STREAMING_OPTION_ENABLED = "1"
    STREAMING_OPTION_DISABLED = "0"


def to_streaming_options_db(streaming_options: List[str]) -> str:
    active_streaming_indices = [STREAMING_OPTIONS.index(streaming_option) for streaming_option in streaming_options]
    streamings_db = [StreamingOptionsCoding.STREAMING_OPTION_DISABLED.value] * len(STREAMING_OPTIONS)
    for ind in active_streaming_indices:
        streamings_db[ind] = StreamingOptionsCoding.STREAMING_OPTION_ENABLED.value
    return "".join(streamings_db)


def from_streaming_options_db(db_streaming: str) -> List[str]:
    streaming_options = []
    for ind in range(len(db_streaming)):
        if db_streaming[ind] == StreamingOptionsCoding.STREAMING_OPTION_ENABLED.value:
            streaming_options.append(STREAMING_OPTIONS[ind])
    return streaming_options
