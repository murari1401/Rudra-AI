import pyautogui
import pytesseract
from PIL import ImageGrab
import time
import os
import subprocess
import platform

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def click_text_on_screen(target_text):
    """Click on the screen where the given text appears using OCR."""
    screen = ImageGrab.grab()
    data = pytesseract.image_to_data(screen, output_type=pytesseract.Output.DICT)
    candidates = []
    for i, word in enumerate(data["text"]):
        if target_text.lower() in word.lower():
            x = data["left"][i] + data["width"][i] // 2
            y = data["top"][i] + data["height"][i] // 2
            candidates.append((word, x, y))
    if not candidates:
        print(f"❌ No match found for: {target_text}")
        return False
    word, x, y = candidates[0]
    print(f"🖱️ Clicking on: {word} at ({x}, {y})")
    pyautogui.moveTo(x, y)
    pyautogui.click()
    return True

def scroll_down():
    print("🌀 Scrolling down slowly...")
    for _ in range(10):
        pyautogui.scroll(-30)
        time.sleep(0.1)

def scroll_up():
    print("🌀 Scrolling up slowly...")
    for _ in range(10):
        pyautogui.scroll(30)
        time.sleep(0.1)

def open_local_app(app_name):
    system = platform.system().lower()
    try:
        if system == "windows":
            app_paths = {
                "notepad": "notepad",
                "calculator": "calc",
                "paint": "mspaint",
                "whatsapp": "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
                "instagram": "shell:AppsFolder\\Facebook.InstagramBeta_8xx8rvfyw5nnt!App",
                "spotify": "shell:AppsFolder\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify"
            }
            if app_name in app_paths:
                os.system(f'start {app_paths[app_name]}')
                return True
        return False
    except Exception as e:
        print(f"❌ Error opening app: {e}")
        return False

def type_text_on_screen(text):
    try:
        pyautogui.write(text, interval=0.05)
        return True
    except Exception as e:
        print(f"❌ Typing error: {e}")
        return False

def close_active_window():
    try:
        pyautogui.hotkey('alt', 'f4')
        return True
    except:
        return False

def switch_to_next_tab():
    pyautogui.hotkey('ctrl', 'tab')

def switch_to_previous_tab():
    pyautogui.hotkey('ctrl', 'shift', 'tab')

def copy_text():
    pyautogui.hotkey('ctrl', 'c')

def paste_text():
    pyautogui.hotkey('ctrl', 'v')

def send_whatsapp_message(contact_name, message):
    try:
        # Make sure WhatsApp window is active
        os.system('start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App')
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.write(contact_name)
        time.sleep(1.5)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.write(message)
        pyautogui.press('enter')
        return True
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {e}")
        return False
