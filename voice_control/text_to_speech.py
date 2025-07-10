import pyttsx3

def speak(text):
  engine = pyttsx3.init()
  voices = engine.getProperty('voices')
  engine.setProperty('voice', voices[0].id)  # Usually male
  engine.setProperty('rate', 160)
  engine.setProperty('volume', 1.0)

  print(f"🗣️ RUDRA: {text}")
  engine.say(text)
  engine.runAndWait()