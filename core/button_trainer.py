import pytesseract
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import time
import os

# Make sure this path is correct
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_screen():
    """Capture a screenshot and return it as an OpenCV image."""
    screenshot = ImageGrab.grab()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def find_and_click_button(app_name, button_text):
    """
    Scan the screen for a button with specific text and click it.
    This uses OCR (pytesseract) to recognize text on screen.
    """
    try:
        print(f"🔍 Searching for '{button_text}' in {app_name}...")
        screen = capture_screen()
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

        for i in range(len(data['text'])):
            text = data['text'][i].strip().lower()
            conf = int(data['conf'][i])

            # Only consider high confidence matches (>85%)
            if text and button_text.lower() in text and conf > 85:
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]

                center_x = x + w // 2
                center_y = y + h // 2

                print(f"✅ Found '{text}' (confidence: {conf}%) at ({center_x}, {center_y})")
                pyautogui.moveTo(center_x, center_y, duration=0.2)
                pyautogui.click()
                return True

        print("❌ Button not found or confidence too low")
        return False

    except Exception as e:
        print(f"🚫 Error in find_and_click_button: {e}")
        return False