# voice_control/speech_input.py
import speech_recognition as sr

def listen_to_user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening for command...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"
