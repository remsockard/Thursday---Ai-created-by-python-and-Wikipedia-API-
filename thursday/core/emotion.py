# core/emotion.py

# This will hold the current emotion of the assistant
current_emotion = "neutral"

def update_emotion(new_emotion):
    global current_emotion
    current_emotion = new_emotion

    # You can link this to a mascot image or animation later
    print(f"[🌀 Emotion Update] Assistant is now feeling: {new_emotion.upper()}")

def get_emotion():
    return current_emotion
