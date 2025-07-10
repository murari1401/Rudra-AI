# core/whatsapp_module.py

import pyautogui
import time
from core.voice_assistant import VoiceAssistant
from core.screen_reader import wait_for_text

va = VoiceAssistant()

def send_whatsapp_message():
    va.speak("Opening WhatsApp")
    pyautogui.hotkey("win", "s")
    pyautogui.write("WhatsApp")
    pyautogui.press("enter")
    time.sleep(5)

    va.speak("Whom do you want to message?")
    contact = va.listen()
    pyautogui.write(contact)
    time.sleep(2)
    pyautogui.press("enter")

    va.speak("What message should I send?")
    message = va.listen()
    va.speak(f"Sending: {message}")
    pyautogui.write(message)
    pyautogui.press("enter")

    va.speak("Message sent.")
