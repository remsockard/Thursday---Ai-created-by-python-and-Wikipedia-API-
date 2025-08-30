# voice/listen.py

import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

def listen_to_user():
    with sr.Microphone() as source:
        print("🎧 Listening...")
        recognizer.adjust_for_ambient_noise(source)  # handles background noise
        audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio)
            return user_input.lower()
        except sr.UnknownValueError:
            print("❗ Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("🚫 Error: Check your internet connection.")
            return None
