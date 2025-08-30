# voice/speak.py

import pyttsx3

# Initialize the TTS engine once
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

def speak_to_user(text):
    print(f"[🗣️ AI] {text}")
    engine.say(text)
    engine.runAndWait()
