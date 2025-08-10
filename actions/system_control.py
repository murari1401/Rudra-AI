import pyautogui

def scroll_down():
    pyautogui.scroll(-500)

def click_button(image_path):
    btn = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)
    if btn:
        pyautogui.click(btn)
