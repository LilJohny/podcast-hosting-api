from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggopus import OggOpus


def get_duration(audio_file, file_kind):
    return file_kind(audio_file).info.length


AUDIO_FILE_KINDS = {
    ".mp3": MP3,
    ".wave": WAVE,
    ".wav": WAVE,
    ".ogg": OggOpus
}
