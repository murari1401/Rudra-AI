# 🔱 RUDRA AI – Your Next-Gen Voice + Gesture Controlled AI Assistant

RUDRA AI is a futuristic desktop AI assistant built using Python and Unity 3D, inspired by Tony Stark’s J.A.R.V.I.S. Named after Lord Shiva, it combines **voice control**, **gesture-based UI interaction**, and **real-time app automation** to deliver a sci-fi-level experience.



---

## 🚀 Features

- 🎙️ **Voice-Controlled Commands**
  - Open apps like WhatsApp, Instagram, YouTube, etc.
  - Perform Wikipedia/web searches
  - Type messages, scroll windows, control system functions
- 🧠 **Smart Decision Engine**
  - Detects if input is a system command or online query
- 🪟 **App UI Control (OCR + AI)**
  - Learns and interacts with app UI (e.g., click buttons inside WhatsApp)
- 👋 **Gesture-Based Hologram UI**
  - Unity 3D-powered interface with drag-and-drop 3D icons
  - Icons orbit around user in sci-fi fashion
- 🧾 **OCR Training System**
  - Auto-learns icon meanings from screen using Tesseract + ML
- 🔄 **Multithreaded Task Execution**
  - Keeps listening while executing commands
- 🗣️ **Custom Voice Feedback**
  - Speaks with a lifelike custom voice
- 🔐 **Coming Soon:**
  - Voice-based login with Hindu mythology integration
  - Real-time safety features for emergency triggers

---

## 🛠️ Tech Stack

| Component            | Tech Used                        |
|----------------------|----------------------------------|
| Core Engine          | Python 3.12                      |
| Speech Recognition   | `speech_recognition`, `pyttsx3` |
| GUI Interaction      | `PyAutoGUI`, `pynput`            |
| OCR & Icon Training  | `OpenCV`, `Pytesseract`, `ML`    |
| 3D UI & Gestures     | Unity 3D + Mediapipe             |
| Hologram Animation   | Unity (C# + Shader Effects)      |
| Web Queries          | Wikipedia API + Custom Search    |
| Threading            | Python `threading` & `queue`     |

---

## 📁 Project Structure

RUDRA_AI/
├── main.py # Main launcher
├── rudra_config.json # Config for personality/voice
├── wakeword/ # Hotword detection (Hey Rudra)
│ └── detect.py
├── voice_control/ # Voice input/output
│ ├── speech_input.py
│ ├── text_to_speech.py
├── gesture_control/ # Hand tracking & gesture actions
│ ├── hand_tracker.py
│ ├── gesture_actions.py
├── actions/ # App launcher, system actions
│ ├── app_launcher.py
│ ├── system_control.py
├── ui/ # Unity hologram UI interface
│ ├── hologram_ui.py
├── models/ # ML models for OCR/icon learning
├── assets/ # Voice files, images, icons
│ └── intro.mp3, icons, etc.
├── requirements.txt
└── README.md

 
---

## ⚙️ How to Run

### 🔹 1. Clone this Repo
```bash
git clone https://github.com/murari1401/RudraAI
cd RUDRA_AI
🔹 2. Set up Virtual Environment
 
python -m venv venv
venv\Scripts\activate   # Windows
🔹 3. Install Python Dependencies
 
pip install -r requirements.txt
🔹 4. Install Tesseract-OCR (for icon recognition)
Download from: https://github.com/tesseract-ocr/tesseract

Add its path to environment variables

🔹 5. Run the Assistant
 
python main.py
✨ Unity UI must be running separately. Launch Unity and open the hologram project before starting Python.

📹 Demo (optional)
You can embed a YouTube video or GIF here showing the working AI.

💡 Inspiration
Inspired by J.A.R.V.I.S. from Iron Man and spiritual symbolism of Rudra (Shiva) – the destroyer of ignorance, the protector in chaos, and the eternal guide.

🙏 Acknowledgements
Mediapipe (Google)

PyTesseract

Unity Technologies

Wikipedia API

Voice & Speech API communities

📬 Contact
Murari | Software Developer & AI Creator
✉️ Email:begarimurari@gmail.com
🔗 GitHub:https://github.com/murari1401
📍 India

⚠️ This is an experimental, evolving project meant for personal AI research and development.

---

