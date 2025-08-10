import subprocess
import pyautogui
import time
import logging
from typing import Tuple, Optional
import os
from PyQt5.QtCore import QObject, pyqtSignal

class CommandProcessor(QObject):
    status_update = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.apps = {
            'whatsapp': 'shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App',
            'instagram': 'shell:AppsFolder\\Facebook.InstagramBeta_8xx8rvfyw5nnt!App',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'chrome': self._get_chrome_path()
        }

    def _get_chrome_path(self) -> str:
        """Get Chrome installation path"""
        possible_paths = [
            os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
            os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
            os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe')
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return ''

    def process_command(self, command: str) -> Tuple[str, Optional[str]]:
        """Process command and return (action_type, response)"""
        command = command.lower().strip()

        try:
            # WhatsApp commands
            if "whatsapp" in command and "message" in command:
                return "action", self._handle_whatsapp_message(command)

            # Instagram commands
            if "instagram" in command:
                return "action", self._handle_instagram(command)

            # App opening commands
            if "open" in command:
                for app, path in self.apps.items():
                    if app in command:
                        success = self._launch_app(app, path)
                        return "app", f"{'Opened' if success else 'Failed to open'} {app}"

            # Code writing commands
            if "write code" in command or "code for" in command:
                return "code", self._handle_code_request(command)

            # System commands
            if "volume" in command:
                return "system", self._handle_volume_command(command)

            return "chat", command  # Default to chat response

        except Exception as e:
            self.logger.error(f"Command processing error: {e}")
            self.error_occurred.emit(str(e))
            return "error", str(e)

    def _launch_app(self, app_name: str, path: str) -> bool:
        """Launch application with proper handling"""
        try:
            if 'shell:AppsFolder' in path:
                subprocess.run(['explorer', path], check=True)
            else:
                subprocess.Popen(path)
            time.sleep(2)  # Wait for app launch
            return True
        except Exception as e:
            self.logger.error(f"Error launching {app_name}: {e}")
            return False

    def _handle_whatsapp_message(self, command: str) -> str:
        """Handle WhatsApp messaging using Desktop app"""
        try:
            # Parse command to get contact and message
            parts = command.split("saying")
            if len(parts) != 2:
                return "Please say: Send WhatsApp message to [contact] saying [message]"

            contact = parts[0].replace("message", "").replace("to", "").strip()
            message = parts[1].strip()

            # Launch WhatsApp Desktop
            subprocess.run(['explorer', self.apps['whatsapp']], check=True)
            time.sleep(4)  # Wait longer for app to load

            # Use Windows keyboard shortcuts
            pyautogui.hotkey('ctrl', 'alt', '/')  # Open search
            time.sleep(1)
            pyautogui.write(contact)
            time.sleep(1.5)
            pyautogui.press('enter')
            time.sleep(1)

            # Write and send message
            pyautogui.write(message)
            time.sleep(0.5)
            pyautogui.press('enter')

            return f"Message sent to {contact}"

        except Exception as e:
            self.logger.error(f"WhatsApp Desktop error: {e}")
            return f"Failed to send message: {str(e)}"

    def _handle_instagram(self, command: str) -> str:
        """Handle Instagram commands"""
        try:
            # Launch Instagram
            success = self._launch_app('instagram', self.apps['instagram'])
            if not success:
                return "Failed to open Instagram"

            time.sleep(3)  # Wait for app to load

            if "profile" in command:
                # Go to profile
                pyautogui.hotkey('ctrl', 'p')
                return "Opened Instagram profile"
            elif "home" in command:
                # Go to home feed
                pyautogui.hotkey('ctrl', 'h')
                return "Opened Instagram home feed"
            elif "explore" in command:
                # Go to explore
                pyautogui.hotkey('ctrl', 'e')
                return "Opened Instagram explore page"
            else:
                return "Opened Instagram"

        except Exception as e:
            self.logger.error(f"Instagram error: {e}")
            return f"Instagram error: {str(e)}"

    def _handle_code_request(self, command: str) -> str:
        """Handle code writing requests"""
        try:
            # Launch notepad
            subprocess.Popen(['notepad.exe'])
            time.sleep(1)

            # Extract language and topic
            code_examples = {
                "python addition": """
def add_numbers(a: float, b: float) -> float:
    return a + b

# Example usage:
result = add_numbers(5, 3)
print(f"5 + 3 = {result}")
""",
                "python hello world": """
def say_hello(name: str = "World") -> None:
    print(f"Hello, {name}!")

# Example usage:
say_hello()
say_hello("User")
"""
            }

            # Find matching example
            for key, code in code_examples.items():
                if all(word in command for word in key.split()):
                    pyautogui.write(code)
                    return f"Code written for {key}"

            return "Sorry, I don't have that code example yet"

        except Exception as e:
            self.logger.error(f"Code writing error: {e}")
            return f"Code writing error: {e}"

    def _handle_volume_command(self, command: str) -> str:
        """Handle volume control commands"""
        try:
            if "up" in command:
                pyautogui.press('volumeup', 5)
                return "Volume increased"
            elif "down" in command:
                pyautogui.press('volumedown', 5)
                return "Volume decreased"
            elif "mute" in command:
                pyautogui.press('volumemute')
                return "Volume muted"
            return "Invalid volume command"
        except Exception as e:
            self.logger.error(f"Volume control error: {e}")
            return f"Volume control error: {e}"