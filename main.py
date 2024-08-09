from ffmpegaudiorecord import start_recording
import os
import subprocess

def record():
    try:
        os.remove("voice.ogg")
    except:
        pass
    audio_data = start_recording(
        ffmpegexe="ffmpeg/bin/ffmpeg.exe", audiodevice=1, silent_seconds_stop=10, silence_threshold=-50)
    with open("voice.raw", "wb") as f:
        f.write(audio_data.raw_data)

    subprocess.run("ffmpeg/bin/ffmpeg.exe -f s16le -ar 44100 -ac 2 -i voice.raw -c:a libvorbis voice.ogg")
    try:
        os.remove("voice.raw")
    except:
        pass


if __name__ == '__main__':
    record()
