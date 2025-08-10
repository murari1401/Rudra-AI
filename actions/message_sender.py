import pywhatkit as pwk
import time
import subprocess
import os
from win32com.client import Dispatch

class AppLauncher:
    def __init__(self):
        self.app_paths = {
            'whatsapp': '5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App',
            'instagram': 'Facebook.InstagramBeta_8xx8rvfyw5nnt!App',
            'notepad': 'Microsoft.WindowsNotepad_8wekyb3d8bbwe!App',
            'calculator': 'Microsoft.WindowsCalculator_8wekyb3d8bbwe!App'
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
            'mummy': '+916302407375',
            'daddy': '+919177391764'
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
