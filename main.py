import os
import time
import datetime
import speech_recognition as sr

GOOGLE_CLOUD_CREDENTIALS_JSON = None
LANG = "en-US"
PHRASE_TIME_LIMIT = 6
OUTPUT_DIR = "recordings"
os.makedirs(OUTPUT_DIR, exist_ok=True)
r = sr.Recognizer()

def save_audio_to_wav(audio_data, filename):
    wav_bytes = audio_data.get_wav_data()
    with open(filename, "wb") as f:
        f.write(wav_bytes)

def timestamped_filename(prefix="record", ext=".wav"):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}_{ts}{ext}"

def listen_and_transcribe():
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                audio = r.listen(source, phrase_time_limit=PHRASE_TIME_LIMIT)
                fname = os.path.join(OUTPUT_DIR, timestamped_filename())
                save_audio_to_wav(audio, fname)
                if GOOGLE_CLOUD_CREDENTIALS_JSON:
                    text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_CREDENTIALS_JSON, language=LANG)
                else:
                    text = r.recognize_google_cloud(audio, language=LANG)
                print("Saved:", fname)
                print("Transcript:", text)
            except sr.RequestError as e:
                print("API Error:", e)
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except KeyboardInterrupt:
                print("Stopped.")
                break
            except Exception as e:
                print("Error:", e)
                time.sleep(0.5)

if __name__ == "__main__":
    listen_and_transcribe()
