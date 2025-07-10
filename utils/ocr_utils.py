import pytesseract
from PIL import ImageGrab

def find_text_on_screen(target_text):
    """Search for text on the screen and return its center coordinates."""
    try:
        screen = ImageGrab.grab()
        data = pytesseract.image_to_data(screen, output_type=pytesseract.Output.DICT)

        for i, word in enumerate(data["text"]):
            if target_text.lower() in word.lower():
                x = data["left"][i] + data["width"][i] // 2
                y = data["top"][i] + data["height"][i] // 2
                return x, y
    except Exception as e:
        print("❌ OCR error:", e)

    return None, None
