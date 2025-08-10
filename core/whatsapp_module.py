# core/whatsapp_module.py

import pyautogui
import time
import subprocess
from typing import Optional
from core.screen_reader import wait_for_text

def open_whatsapp() -> bool:
    """Open WhatsApp Desktop app"""
    try:
        subprocess.run(['explorer', 'shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App'])
        return wait_for_text("WhatsApp", 10)
    except Exception as e:
        print(f"❌ Error opening WhatsApp: {e}")
        return False

def search_contact(name: str) -> bool:
    """Search for a contact in WhatsApp"""
    try:
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.write(name)
        return wait_for_text(name, 5)
    except Exception as e:
        print(f"❌ Error searching contact: {e}")
        return False

def type_message(message: str) -> bool:
    """Type message in WhatsApp"""
    try:
        pyautogui.write(message)
        return True
    except Exception as e:
        print(f"❌ Error typing message: {e}")
        return False

def send_message() -> bool:
    """Send message in WhatsApp"""
    try:
        pyautogui.press('enter')
        return True
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False
