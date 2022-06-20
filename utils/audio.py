import av
from mutagen.mp3 import MP3
from mutagen.oggopus import OggOpus
from mutagen.wave import WAVE


def get_duration(audio_file, file_kind):
    return file_kind(audio_file).info.length


AUDIO_FILE_KINDS = {
    ".mp3": MP3,
    ".wave": WAVE,
    ".wav": WAVE,
    ".ogg": OggOpus
}


def decode_webm_to_mp3(webm_file):
    with av.open(webm_file, 'r') as inp:
        out = av.open("temp.mp3", 'w', format="mp3")
        out_stream = out.add_stream("mp3")
        for frame in inp.decode(audio=0):
            frame.pts = None
            for packets in out_stream.encode(frame):
                out.mux(packets)
        for packets in out_stream.encode(None):
            out.mux(packets)

    return open("temp.mp3", "rb")
