import winsound
import threading
from typing import Optional

class VoiceFeedback:
    def __init__(self):
        self.beep_thread = None

    def acknowledge_command(self):
        """Play a short acknowledgment tone"""
        self._play_beep(1000, 100)  # 1kHz for 100ms

    def indicate_listening(self):
        """Play a listening indicator tone"""
        self._play_beep(800, 200)  # 800Hz for 200ms

    def indicate_error(self):
        """Play an error tone"""
        self._play_beep(400, 300)  # 400Hz for 300ms

    def _play_beep(self, frequency: int, duration: int):
        """Play beep in separate thread to avoid blocking"""
        if self.beep_thread and self.beep_thread.is_alive():
            return

        def beep():
            try:
                winsound.Beep(frequency, duration)
            except Exception as e:
                print(f"❌ Audio feedback error: {e}")

        self.beep_thread = threading.Thread(target=beep)
        self.beep_thread.daemon = True
        self.beep_thread.start()