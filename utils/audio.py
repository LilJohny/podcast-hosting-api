from mutagen.mp3 import MP3
from mutagen.wave import WAVE


def get_duration_mp3(audio_file):
    return MP3(audio_file).info.length


def get_duration_wave(audio_file):
    return WAVE(audio_file).info.length


DURATION_FINDERS = {
    ".mp3": get_duration_mp3,
    ".wave": get_duration_wave,
    ".wav": get_duration_wave
}
