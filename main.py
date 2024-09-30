from ffmpegaudiorecord import start_recording
import os
import subprocess
import settings
from openai import OpenAI

# Initialisierung des OpenAI-Clients mit dem API-Schlüssel aus den Einstellungen
openai_client = OpenAI(api_key=settings.api_key)
history = []


def record():
    """Nimmt Audio auf, konvertiert es und bereinigt temporäre Dateien."""
    # Versuch, bestehende Audiodatei zu löschen
    try:
        os.remove("voice.ogg")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Fehler beim Löschen der Datei 'voice.ogg': {e}")

    print("PROGRESS: Aufnahme läuft...", end="")
    audio_data = start_recording(
        ffmpegexe=settings.record_ffmpegexe,
        audiodevice=settings.record_audiodevice,
        silent_seconds_stop=settings.record_silent_seconds_stop,
        silence_threshold=settings.record_silence_threshold
    )

    print("\rPROGRESS: Konvertiere Audio...", end="")
    with open("voice.raw", "wb") as f:
        f.write(audio_data.raw_data)

    # Ausführen von FFmpeg zum Konvertieren der Rohdatei in eine OGG-Datei
    subprocess.run([
        settings.record_ffmpegexe,
        '-f', 's16le',
        '-ar', '44100',
        '-ac', '2',
        '-i', 'voice.raw',
        '-c:a', 'libvorbis',
        'voice.ogg'
    ],  stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE)

    print("\rPROGRESS: Bereinige temporäre Dateien...", end="")
    try:
        os.remove("voice.raw")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Fehler beim Löschen der Datei 'voice.raw': {e}")
    print("\r                                        ",end="")


def transcribe():
    """Transkribiert die Audiodatei mit dem OpenAI-Transkriptionsservice."""
    print("\rPROGRESS: Transkribiere Audio...", end="")
    try:
        with open("voice.ogg", "rb") as audio_file:
            transcription = openai_client.audio.transcriptions.create(
                model=settings.transcribe_model,
                file=audio_file
            )
        print(f"\rUser: {transcription.text}")
        return transcription.text
    except Exception as e:
        print(f"Fehler bei der Transkription: {e}")


def addToChat(role, message):
    """Fügt eine Nachricht zur Chat-Historie hinzu."""
    valid_roles = ['system', 'assistant', 'user']
    if role.lower() not in valid_roles:
        print(f"Ungültige Rolle: {role}. Erlaubte Rollen sind: {', '.join(valid_roles)}.")
        return
    history.append({'role': role.lower(), 'content': message})


def chat(history):
    """Erzeugt eine Antwort basierend auf der Chat-Historie."""
    print("PROGRESS: Generiere Antwort...", end="")
    try:
        response = openai_client.chat.completions.create(
            model=settings.chat_model,
            messages=history
        )
        assistant_message = response.choices[0].message.content
        print(f"\rAssistent: {assistant_message}")
        # Füge die Antwort des Assistenten zur Chat-Historie hinzu
        addToChat('assistant', assistant_message)
        return assistant_message
    except Exception as e:
        print(f"Fehler beim Generieren der Antwort: {e}")
        return ""


def tts(text):
    response= openai_client.audio.speech.create(
        input=text,
        model=settings.tts_model,
        voice=settings.tts_voice,
        response_format="mp3"
    )
    c = response.content
    with open("response.mp3","wb") as f:
        f.write(c)

    subprocess.run([
        "mpv",
        "response.mp3"
    ])

DEV=False
if __name__ == '__main__':
    if not DEV:
        while True:
            record()
            text = transcribe()
            if text.lower().startswith("exit"):
                print("Programm wird beendet.")
                break
            addToChat("user", text)
            text = chat(history)
            tts(text)
    else:
        addToChat("user", "Hallo, wie macht die Kuh?")
        text = chat(history)
        tts(text)