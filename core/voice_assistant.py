import pyttsx3
import sounddevice as sd
import queue
import json
import vosk
import wikipedia
import threading
import os


class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.q = queue.Queue()
        self.model_path = "vosk-model-en-us-0.22"

        if not os.path.exists(self.model_path):
            raise FileNotFoundError("❌ Vosk model not found. Download from https://alphacephei.com/vosk/models and extract to project root.")

        self.model = vosk.Model(self.model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.samplerate = 16000

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def safe_speak(self, text):
        threading.Thread(target=self.speak, args=(text,), daemon=True).start()

    def callback(self, indata, frames, time, status):
        if status:
            print("⚠️", status)
        self.q.put(bytes(indata))

    def listen(self):
        print("🎙️ Listening...")
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, dtype='int16',
                               channels=1, callback=self.callback):
            while True:
                data = self.q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    text = json.loads(result).get("text", "")
                    if text:
                        print(f"🧠 You said: {text}")
                        return text.lower()
                    else:
                        print("🤖 Didn't catch that.")
                        return ""

    def handle_query(self, query):
        try:
            self.safe_speak("🌐 Searching Wikipedia for: " + query)
            summary = wikipedia.summary(query, sentences=2)
            self.safe_speak(summary)
        except Exception as e:
            print("❌ Wikipedia Error:", e)
            self.safe_speak("I couldn't find information on that.")
