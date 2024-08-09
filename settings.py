
# get of api.key file and assuming its correct...
try:
    with open("api.key", "r") as f:
        api_key = f.readline()
except FileNotFoundError:
    open("api.key", "w").write("JustReplaceMe")
    print("api.key file created...")
    print("please go to https://platform.openai.com/api-keys")
    print("to create an new apikey")
    exit()

record_audiodevice=0
record_silent_seconds_stop=3
record_silence_threshold=-50
record_ffmpegexe="ffmpeg/bin/ffmpeg.exe"

transcribe_model = "whisper-1"
