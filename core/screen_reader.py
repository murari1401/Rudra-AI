# core/screen_reader.py

import pytesseract
from PIL import ImageGrab
import time
from core.rudra_memory import remember_element

# ✅ STEP 1: Point to your Tesseract installation
# (Make sure this path matches where you installed it)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ STEP 2: Read full screen as text (used for answering questions, interface detection)
def scan_screen_text():
    """Capture the full screen and return detected text."""
    screen = ImageGrab.grab()
    return pytesseract.image_to_string(screen)

# ✅ STEP 3: Scan screen and remember every word as a UI element (like button text)
def scan_visible_buttons():
    """Scan screen and remember clickable words/buttons."""
    screen = ImageGrab.grab()
    data = pytesseract.image_to_data(screen, output_type=pytesseract.Output.DICT)

    for i, word in enumerate(data["text"]):
        if word.strip() and int(data["conf"][i]) > 60:  # Confidence above 60%
            remember_element(word.strip().lower())

# ✅ STEP 4: Run once on startup to prepare memory
def initialize_ocr_memory():
    """Initial OCR memory setup on boot."""
    print("🔍 Scanning screen for visible UI elements...")
    scan_visible_buttons()

def wait_for_text(text: str, timeout: int = 10) -> bool:
    """
    Wait for text to appear on screen

    Args:
        text: Text to search for
        timeout: Maximum time to wait in seconds

    Returns:
        bool: True if text found, False if timeout
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            screen = ImageGrab.grab()
            screen_text = pytesseract.image_to_string(screen).lower()
            if text.lower() in screen_text:
                return True
        except Exception as e:
            print(f"❌ Screen reading error: {e}")
        time.sleep(0.5)
    return False
