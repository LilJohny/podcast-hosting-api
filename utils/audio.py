from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.ogg import OggFileType


def get_duration_mp3(audio_file):
    return MP3(audio_file).info.length


def get_duration_wave(audio_file):
    return WAVE(audio_file).info.length


def get_duration_ogg(audio_file):
    return OggFileType(audio_file).info.length


DURATION_FINDERS = {
    ".mp3": get_duration_mp3,
    ".wave": get_duration_wave,
    ".wav": get_duration_wave,
    ".ogg": get_duration_ogg
}
