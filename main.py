from ffmpegaudiorecord import start_recording
import os
import subprocess
import settings
from openai import OpenAI

openai_client = OpenAI(api_key=settings.api_key)
history = []


def record():
    try:
        os.remove("voice.ogg")
    except:
        pass
    print("recording...", end="")
    audio_data = start_recording(
        ffmpegexe=settings.record_ffmpegexe,
        audiodevice=settings.record_audiodevice,
        silent_seconds_stop=settings.record_silent_seconds_stop,
        silence_threshold=settings.record_silence_threshold
    )
    print("DONE")
    print("converting...", end="")
    with open("voice.raw", "wb") as f:
        f.write(audio_data.raw_data)

    subprocess.run(f"{settings.record_ffmpegexe} -f s16le -ar 44100 -ac 2 -i voice.raw -c:a libvorbis voice.ogg",
                   stdout=subprocess.DEVNULL)
    print("DONE")
    print("cleanup...", end="")
    try:
        os.remove("voice.raw")
    except:
        pass
    print("DONE")


def transcribe():
    print("transcribing...", end="")
    audio_file = open("voice.ogg", "rb")
    transcription = openai_client.audio.transcriptions.create(
        model=settings.transcribe_model,
        file=audio_file
    )
    print("DONE")
    print(transcription.text)


if __name__ == '__main__':
    record()
    transcribe()
