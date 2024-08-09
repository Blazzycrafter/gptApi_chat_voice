from ffmpegaudiorecord import start_recording
import os
import subprocess
import settings


def record():
    try:
        os.remove("voice.ogg")
    except:
        pass
    audio_data = start_recording(
        ffmpegexe=settings.record_ffmpegexe,
        audiodevice=settings.record_audiodevice,
        silent_seconds_stop=settings.record_silent_seconds_stop,
        silence_threshold=settings.record_silence_threshold
    )
    with open("voice.raw", "wb") as f:
        f.write(audio_data.raw_data)

    subprocess.run(f"{settings.record_ffmpegexe} -f s16le -ar 44100 -ac 2 -i voice.raw -c:a libvorbis voice.ogg")
    try:
        os.remove("voice.raw")
    except:
        pass


if __name__ == '__main__':
    record()

# THIS COMMENT OLNY EXIST FOR REFORMATTING
