import os
import time
import subprocess
import platform
import pyautogui
import pytesseract
from PIL import ImageGrab

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ----------------------------
# OCR-BASED INTERACTIONS
# ----------------------------

def click_text_on_screen(target_text: str, confidence: float = 0.8) -> bool:
    """Locate text on screen via OCR and click its center."""
    screen = ImageGrab.grab()
    data = pytesseract.image_to_data(screen, output_type=pytesseract.Output.DICT)
    for i, word in enumerate(data["text"]):
        if target_text.lower() in word.lower():
            x = data["left"][i] + data["width"][i] // 2
            y = data["top"][i] + data["height"][i] // 2
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(0.5)
            return True
    return False

# ----------------------------
# MOUSE & SCROLL CONTROLS
# ----------------------------

def scroll_down(amount: int = 300):
    """Scroll down by a specified amount."""
    pyautogui.scroll(-amount)


def scroll_up(amount: int = 300):
    """Scroll up by a specified amount."""
    pyautogui.scroll(amount)

# ----------------------------
# APPLICATION LAUNCHING
# ----------------------------

def open_local_app(app_name: str) -> bool:
    """Open common local apps via system commands or store shortcuts."""
    system = platform.system().lower()
    if system != "windows":
        return False

    mapping = {
        "notepad": "notepad",
        "calculator": "calc",
        "paint": "mspaint",
        "whatsapp": "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
        "instagram": "shell:AppsFolder\\Facebook.InstagramBeta_8xx8rvfyw5nnt!App",
        "spotify": "shell:AppsFolder\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify"
    }
    key = app_name.lower().strip()
    cmd = mapping.get(key)
    if not cmd:
        return False
    subprocess.run(["cmd", "/C", f"start {cmd}"], shell=True)
    time.sleep(2)
    return True

# ----------------------------
# TYPING & WINDOW CONTROLS
# ----------------------------

def type_text_on_screen(text: str, interval: float = 0.05) -> bool:
    """Type text at current cursor position."""
    try:
        pyautogui.write(text, interval=interval)
        return True
    except Exception:
        return False


def close_active_window():
    """Close currently active window."""
    pyautogui.hotkey('alt', 'f4')
    return True


def switch_to_next_tab():
    """Switch to next browser tab."""
    pyautogui.hotkey('ctrl', 'tab')


def switch_to_previous_tab():
    """Switch to previous browser tab."""
    pyautogui.hotkey('ctrl', 'shift', 'tab')


def copy_text():
    """Copy selected text to clipboard."""
    pyautogui.hotkey('ctrl', 'c')


def paste_text():
    """Paste text from clipboard."""
    pyautogui.hotkey('ctrl', 'v')

# ----------------------------
# WHATSAPP WEB AUTOMATION
# ----------------------------
try:
    import pywhatkit as pwk
except ImportError:
    pwk = None


def send_whatsapp_web(contact: str, message: str, wait_time: int = 10) -> bool:
    """Send WhatsApp message via web (pywhatkit)."""
    if pwk is None:
        return False
    try:
        # Assumes contact is in format +CountryCodeNumber
        pwk.sendwhatmsg_instantly(contact, message, wait_time=wait_time, tab_close=True)
        return True
    except Exception:
        return False