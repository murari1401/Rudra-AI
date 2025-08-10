from core.voice_assistant import VoiceAssistant
import pyautogui
import time
from typing import Optional
from PIL import ImageGrab
import pytesseract

class WhatsAppHandler:
    def __init__(self, voice_assistant: VoiceAssistant):
        self.va = voice_assistant
        self.retry_delay = 1
        self.max_retries = 3
        self.is_open = False

    def open_whatsapp(self) -> bool:
        """Open WhatsApp desktop app"""
        try:
            subprocess.Popen(['WhatsApp.exe'])
            time.sleep(3)
            self.is_open = True
            return True
        except Exception as e:
            print(f"❌ WhatsApp error: {e}")
            return False

    def send_message(self, contact: str, message: str) -> bool:
        """Send WhatsApp message with retries and verification"""
        for attempt in range(self.max_retries):
            try:
                if not self.is_open:
                    if not self.open_whatsapp():
                        continue

                # Clear search field
                pyautogui.hotkey('ctrl', 'f')
                time.sleep(0.5)
                pyautogui.write(contact)
                time.sleep(2)  # Wait for search results

                # Verify contact found
                if not self.verify_contact_visible(contact):
                    raise Exception("Contact not found")

                pyautogui.press('enter')
                time.sleep(1)

                # Type and send message
                pyautogui.write(message)
                time.sleep(0.5)
                pyautogui.press('enter')
                return True

            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    self.va.safe_speak("Retrying to send message...")
                    time.sleep(self.retry_delay)

        return False

    def verify_contact_visible(self, contact: str) -> bool:
        """Verify contact is visible in search results"""
        screen = ImageGrab.grab()
        text = pytesseract.image_to_string(screen).lower()
        return contact.lower() in text

    def handle_whatsapp_command(self, initial_command):
        if not self._ensure_whatsapp_open():
            return False

        if "send message" in initial_command:
            return self._handle_message_flow()
        else:
            self.va.safe_speak("WhatsApp is ready. Would you like to send a message?")
            response = self.va.listen()
            if response and "yes" in response.lower():
                return self._handle_message_flow()
            return True

    def _ensure_whatsapp_open(self):
        """Ensures WhatsApp is open with retries"""
        for attempt in range(self.max_retries):
            if self.open_whatsapp():
                time.sleep(2)  # Wait for WhatsApp to fully load
                return True
            if attempt < self.max_retries - 1:
                self.va.safe_speak("Having trouble opening WhatsApp. Retrying...")
                time.sleep(self.retry_delay)

        self.va.safe_speak("Sorry, I couldn't open WhatsApp.")
        return False

    def _handle_message_flow(self):
        """Handles the message sending flow"""
        try:
            # Ask for contact
            self.va.safe_speak("Who would you like to message?")
            contact = self.va.listen()
            if not contact:
                self.va.safe_speak("I didn't catch the contact name.")
                return False

            # Search for contact
            if not search_contact(contact):
                self.va.safe_speak(f"Sorry, I couldn't find {contact}")
                return False

            # Get message content
            self.va.safe_speak("What message should I send?")
            message = self.va.listen()
            if not message:
                self.va.safe_speak("I didn't catch the message.")
                return False

            # Confirm before sending
            self.va.safe_speak(f"Should I send '{message}' to {contact}?")
            confirmation = self.va.listen()

            if confirmation and any(word in confirmation.lower() for word in ["yes", "sure", "okay", "send"]):
                if type_message(message) and send_message():
                    self.va.safe_speak("Message sent successfully.")
                    return True
                else:
                    self.va.safe_speak("Sorry, I couldn't send the message.")
                    return False
            else:
                self.va.safe_speak("Message cancelled.")
                return False

        except Exception as e:
            print(f"❌ Error in WhatsApp flow: {e}")
            self.va.safe_speak("Sorry, there was an error with WhatsApp.")
            return False