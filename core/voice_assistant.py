from PyQt5.QtCore import QObject, pyqtSignal
import pyttsx3
import speech_recognition as sr
from openai import OpenAI
import logging
from typing import Optional
from .command_processor import CommandProcessor

class VoiceAssistant(QObject):
    command_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    status_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.command_processor = CommandProcessor()
        self.setup_voice()
        self.setup_recognition()
        self.setup_openai()

    def setup_voice(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 175)
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id)
            logging.info("Voice setup complete")
        except Exception as e:
            logging.error(f"Voice setup error: {e}")
            self.error_occurred.emit(str(e))

    def setup_recognition(self):
        try:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
            logging.info("Recognition setup complete")
        except Exception as e:
            logging.error(f"Recognition setup error: {e}")
            self.error_occurred.emit(str(e))

    def setup_openai(self):
        self.openai_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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"
        )

    def speak(self, text: str):
        try:
            self.status_changed.emit(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"Speech error: {e}")
            self.error_occurred.emit(str(e))

    def listen(self) -> Optional[str]:
        try:
            with sr.Microphone() as source:
                self.status_changed.emit("Listening...")
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=5)

            text = self.recognizer.recognize_google(audio)
            self.command_received.emit(text)
            return text.lower()

        except sr.UnknownValueError:
            self.status_changed.emit("Could not understand audio")
            return None
        except Exception as e:
            self.error_occurred.emit(str(e))
            return None

    def process_command(self, command: str):
        try:
            action_type, response = self.command_processor.process_command(command)

            if action_type == "error":
                self.error_occurred.emit(response)
            elif action_type == "chat":
                # Handle with OpenAI
                self._process_chat(command)
            else:
                self.speak(response)

        except Exception as e:
            self.error_occurred.emit(str(e))

    def _process_chat(self, command: str):
        try:
            self.status_changed.emit("Processing...")
            response = self.openai_client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://rudra-ai.murari.dev",
                    "X-Title": "RUDRA AI Assistant",
                },
                model="openai/gpt-4o",
                messages=[{"role": "user", "content": command}],
                max_tokens=500
            )
            answer = response.choices[0].message.content
            self.speak(answer)

        except Exception as e:
            self.error_occurred.emit(str(e))