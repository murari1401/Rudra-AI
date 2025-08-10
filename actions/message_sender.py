import pywhatkit as pwk
import time
import subprocess
import os
from win32com.client import Dispatch

class AppLauncher:
    def __init__(self):
        self.app_paths = {
            'whatsapp': 'whatsapp location in your pc',
            'instagram': 'instagram location in your pc',
            'notepad': 'notepad locatio in your pc',
            'calculator': 'calculator location in your pc'
        }

    def open_app(self, app_name: str) -> bool:
        try:
            app_id = self.app_paths.get(app_name.lower())
            if app_id:
                subprocess.run(['explorer.exe', f'shell:AppsFolder\{app_id}'])
                time.sleep(1)  # Brief wait for app to launch
                return True
            return False
        except Exception:
            return False

class WhatsAppSender:
    def __init__(self):
        self.contact_map = {
            'mummy': 'add phone number',
            'daddy': 'you can add phone number too'
        }
        self.app_launcher = AppLauncher()

    def send_message(self, contact: str, message: str) -> tuple[bool, str]:
        """Send WhatsApp message with improved handling"""
        try:
            contact = contact.lower().strip()
            number = self.contact_map.get(contact)

            if not number:
                return False, f"Contact '{contact}' not found"

            # Launch WhatsApp first
            self.app_launcher.open_app('whatsapp')
            time.sleep(2)  # Wait for WhatsApp to open

            # Send message
            pwk.sendwhatmsg_instantly(
                number,
                message,
                wait_time=15,  # Increased wait time
                tab_close=True
            )

            return True, f"Message sent to {contact}"

        except Exception as e:
            return False, f"Failed to send message: {str(e)}"

