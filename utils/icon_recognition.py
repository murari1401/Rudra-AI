import cv2
import numpy as np
import pyautogui
import os

ICON_FOLDER = "assets/icons"

def find_and_click_icon(icon_name, threshold=0.75):
    try:
        icon_path = os.path.join(ICON_FOLDER, f"{icon_name}.png")
        if not os.path.exists(icon_path):
            print(f"❌ Icon not found: {icon_path}")
            return False

        screen = pyautogui.screenshot()
        screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        icon = cv2.imread(icon_path)

        result = cv2.matchTemplate(screen_np, icon, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            icon_h, icon_w = icon.shape[:2]
            center_x = max_loc[0] + icon_w // 2
            center_y = max_loc[1] + icon_h // 2
            pyautogui.moveTo(center_x, center_y)
            pyautogui.click()
            print(f"✅ Clicked on icon: {icon_name}")
            return True
        else:
            print(f"❌ Icon {icon_name} not found with sufficient confidence.")
            return False

    except Exception as e:
        print(f"❌ Error in icon detection: {e}")
        return False
