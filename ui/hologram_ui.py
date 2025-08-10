# ui/hologram_ui.py

import cv2
import os
import pyttsx3
import numpy as np
import mediapipe as mp
import webbrowser
import time
import speech_recognition as sr
import threading
import pytesseract
from PIL import ImageGrab, Image, ImageSequence
import pyautogui
import difflib
import platform
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# === CONSTANTS ===
RUDRA_HOLOGRAM_WINDOW = "RUDRA Hologram"

# === GLOBALS ===
current_query = ""
show_voice_animation = False
context_memory = []
gif_frames = []
gif_index = 0
scroll_down_gesture_triggered = False
object_hold_detected = False

# === LOAD VOICE WAVE GIF ===
def load_gif_frames(path):
    frames = []
    try:
        with Image.open(path) as im:
            for frame in ImageSequence.Iterator(im):
                frame = frame.convert("RGBA")
                frame = frame.resize((200, 200))
                frames.append(np.array(frame))
    except Exception as e:
        print("❌ Failed to load Siri wave GIF:", e)
    return frames

# === VOICE OUTPUT ===
def speak(text):
    global current_query, show_voice_animation
    print(f"✨ Speaking: {text}")
    current_query = text
    show_voice_animation = False
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "zira" in voice.name.lower() or "male" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 170)
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass

# === VOICE INPUT ===
def listen():
    global current_query, show_voice_animation
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        show_voice_animation = True
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            print(f"🔣 You said: {text}")
            current_query = text
            context_memory.append(text.lower())
            return text.lower()
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return ""
        except Exception as e:
            print(f"❌ Error during listening: {e}")
            return ""

# === OVERLAY GIF ON FRAME ===
def overlay_gif(frame, gif_frame, x, y):
    h, w = gif_frame.shape[:2]
    for i in range(h):
        for j in range(w):
            alpha = gif_frame[i, j, 3] / 255.0
            if y+i < frame.shape[0] and x+j < frame.shape[1]:
                for c in range(3):
                    frame[y+i, x+j, c] = alpha * gif_frame[i, j, c] + (1 - alpha) * frame[y+i, x+j, c]

# === INTRO VIDEO OR FALLBACK ===
def play_intro():
    intro_path = os.path.join("assets", "intro.mp4")
    if not os.path.exists(intro_path):
        print("⚠️ Intro video not found.")
        speak("Rudra welcomes you sir! Ready to help anytime!")
        return
    cap = cv2.VideoCapture(intro_path)
    cv2.namedWindow("Intro", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Intro", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (1920, 1080))
        cv2.imshow("Intro", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    speak("Rudra welcomes you sir! Ready to help anytime!")

# === APP OPENING FUNCTION ===
def open_app(app_name):
    try:
        if app_name == "whatsapp":
            webbrowser.open("https://web.whatsapp.com")
        elif app_name == "instagram":
            webbrowser.open("https://www.instagram.com")
        elif app_name == "youtube":
            webbrowser.open("https://youtube.com")
        elif app_name == "music":
            os.system("start wmplayer")
    except Exception as e:
        print(f"❌ Failed to open {app_name}: {e}")

# === OCR FUNCTIONS ===
def scan_screen_text():
    screen = ImageGrab.grab()
    return pytesseract.image_to_string(screen)

def click_text_on_screen(text):
    screen = ImageGrab.grab()
    data = pytesseract.image_to_data(screen, output_type=pytesseract.Output.DICT)
    candidates = []
    for i, word in enumerate(data["text"]):
        if text.lower() in word.lower():
            x = data["left"][i] + data["width"][i] // 2
            y = data["top"][i] + data["height"][i] // 2
            candidates.append((word, x, y))
    if len(candidates) == 1:
        pyautogui.moveTo(candidates[0][1], candidates[0][2])
        pyautogui.click()
        return True
    elif len(candidates) > 1:
        speak("Multiple options found. Please say which one.")
        for idx, (word, x, y) in enumerate(candidates):
            speak(f"Option {idx+1}: {word}")
        choice = listen()
        for word, x, y in candidates:
            if choice in word.lower():
                pyautogui.moveTo(x, y)
                pyautogui.click()
                return True
    return False

# === HAND GESTURE SCROLLING AND OBJECT HOLD ===
def detect_hand_gesture(mp_hands, hands, frame):
    global scroll_down_gesture_triggered, object_hold_detected
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

            # Scroll gesture
            if index_tip - thumb_tip > 0.1 and not scroll_down_gesture_triggered:
                pyautogui.scroll(-200)
                scroll_down_gesture_triggered = True
            elif index_tip - thumb_tip <= 0.05:
                scroll_down_gesture_triggered = False

            # Object hold gesture
            if abs(index_tip - middle_tip) < 0.02:
                object_hold_detected = True
            else:
                object_hold_detected = False

# === HANDLE VOICE COMMANDS (Refactored) ===
def process_exit(query):
    if "exit" in query:
        speak("Goodbye, sir!")
        os._exit(0)
        return True
    return False

def process_scroll(query):
    if "scroll down" in query:
        for _ in range(10):
            pyautogui.scroll(-30)
            time.sleep(0.1)
        speak("Scrolling down")
        return True
    return False

def process_open(query):
    for app in ["instagram", "whatsapp", "youtube", "music"]:
        if f"open {app}" in query or (app in query and "open" in query):
            speak(f"Opening {app}")
            open_app(app)
            return True
    return False

def process_close(query):
    if "close" in query:
        speak("Closing current window")
        pyautogui.hotkey("alt", "f4")
        return True
    return False

def process_greeting(query):
    if "hello" in query or "hi rudra" in query:
        speak("Hello sir! How can I assist you today?")
        return True
    return False

def process_click(query):
    found = click_text_on_screen(query)
    if found:
        speak(f"Clicked on {query}")
    else:
        speak(f"You said: {query}")

def handle_voice():
    global current_query
    while True:
        query = listen()
        if not query:
            speak("I didn't catch that. Do you want to try again?")
            continue

        if process_exit(query):
            continue
        if process_scroll(query):
            continue
        if process_open(query):
            continue
        if process_close(query):
            continue
        if process_greeting(query):
            continue

        process_click(query)

# === MAIN ===
def run_hologram_ui():
    global gif_frames, gif_index
    gif_frames = load_gif_frames("assets/siri_wave.gif")

    mp_selfie = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    if not cap.isOpened():
        print("❌ Failed to access webcam")
        return
    print("📸 Webcam accessed successfully.")

    threading.Thread(target=handle_voice, daemon=True).start()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_selfie.process(rgb_frame)
        mask = results.segmentation_mask
        condition = np.stack((mask,) * 3, axis=-1) > 0.6
        frame = np.where(condition, frame, np.zeros(frame.shape, dtype=np.uint8))

        detect_hand_gesture(mp_hands, hands, frame)

        if show_voice_animation and gif_frames:
            overlay_gif(frame, gif_frames[gif_index % len(gif_frames)], 50, frame.shape[0] - 250)
            gif_index += 1

        overlay_text = "RUDRA Virtual Assistant"
        cv2.putText(frame, overlay_text, (600, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

        cv2.namedWindow(RUDRA_HOLOGRAM_WINDOW, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(RUDRA_HOLOGRAM_WINDOW, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(RUDRA_HOLOGRAM_WINDOW, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

class HologramUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components"""
        self.setWindowTitle('RUDRA AI Assistant')
        self.setGeometry(100, 100, 800, 600)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create layout
        layout = QVBoxLayout(central_widget)

        # Add status label
        self.status_label = QLabel("RUDRA AI Ready...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont('Arial', 14))
        layout.addWidget(self.status_label)

        # Style the window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #00ff00;
                padding: 10px;
            }
        """)

    def update_status(self, message: str):
        """Update the status display"""
        self.status_label.setText(message)

if __name__ == "__main__":
    play_intro()
    run_hologram_ui()
