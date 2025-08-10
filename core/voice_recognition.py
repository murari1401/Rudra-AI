import speech_recognition as sr
import sounddevice as sd
import numpy as np
import logging
from typing import Optional
import time
import wave  # Use wave instead of aifc

class VoiceRecognitionManager:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.setup_recognition()

    def setup_recognition(self):
        """Configure recognition settings"""
        try:
            with self.microphone as source:
                # Configure for better recognition
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.recognizer.energy_threshold = 4000
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8

                # Configure audio settings
                self.sample_rate = 16000
                self.channels = 1

            logging.info("✅ Voice recognition initialized")
        except Exception as e:
            logging.error(f"❌ Recognition setup failed: {e}")

    def listen(self) -> Optional[str]:
        """Listen for voice input"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=5
                )

                print("🔍 Processing...")
                text = self.recognizer.recognize_google(audio)
                print(f"🗣️ Heard: {text}")
                return text.lower()

        except sr.WaitTimeoutError:
            print("⌛ No speech detected")
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
        except sr.RequestError as e:
            print(f"🌐 Service error: {str(e)}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            logging.error(f"Recognition error: {e}")

        return None

    def is_speaking(self) -> bool:
        """Check if user is currently speaking"""
        try:
            with sd.Stream(
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=1024
            ) as stream:
                data, _ = stream.read(1024)
                return np.abs(data).mean() > 0.01
        except Exception:
            return False