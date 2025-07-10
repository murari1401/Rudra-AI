import cv2
import mediapipe as mp
import pyttsx3
import os

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def run_gesture_control():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get index finger tip (landmark 8)
                h, w, _ = img.shape
                x = int(hand_landmarks.landmark[8].x * w)
                y = int(hand_landmarks.landmark[8].y * h)

                cv2.circle(img, (x, y), 15, (255, 0, 0), cv2.FILLED)
                print(f"🖐️ Tip of index finger: ({x}, {y})")

                # Trigger based on position
                if x < 100 and y < 100:
                    speak("Opening browser")
                    os.system("start chrome")
                elif x > 500 and y < 100:
                    speak("Playing music")
                    # You can add real music logic
                elif y > 400:
                    speak("Exiting gesture mode")
                    cap.release()
                    cv2.destroyAllWindows()
                    return

        cv2.imshow("RUDRA Gesture Mode", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
