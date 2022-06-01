from mutagen.mp3 import MP3
from mutagen.wave import WAVE


def determine_mp3(audio_file):
    return MP3(audio_file).info.length


def determine_wave(audio_file):
    return WAVE(audio_file).info.length


DURATION_FINDERS = {
    "mp3": determine_mp3,
    "wave": determine_wave
}


