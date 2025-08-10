# voice_control/text_to_speech.py
import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Female voice

def speak(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()
