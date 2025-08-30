import random
import re
import wikipedia

# ✅ Use relative import to avoid ModuleNotFoundError
from .memory_core import get_fact


# Optional: Offline language model using transformers
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
    print("Device set to use cpu")

except Exception as e:
    print("⚠️ Local model not loaded:", e)
    generator = None

# Emotion Triggers
emotion_triggers = {
    "happy": ["thank you", "thanks", "so happy", "good news"],
    "sad": ["i'm sad", "i feel down", "heartbroken"],
    "angry": ["you are wrong", "not correct", "angry"],
    "excited": ["i'm excited", "pumped"],
    "tired": ["i'm tired", "exhausted", "no energy"],
    "lonely": ["i feel lonely", "alone", "no one cares"]
}

# Fun responses
jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why was the math book sad? Because it had too many problems.",
    "What do you call fake spaghetti? An impasta!"
]

facts = [
    "Did you know? The Eiffel Tower can be 15 cm taller during hot days.",
    "Honey never spoils. Archaeologists have found 3,000-year-old honey in tombs!",
    "Bananas are berries, but strawberries aren't."
]

def detect_emotion(user_input):
    for emotion, phrases in emotion_triggers.items():
        for phrase in phrases:
            if phrase in user_input:
                return emotion
    return "neutral"

def answer_general_question(user_input):
    # Try offline model first
    if generator:
        try:
            result = generator(user_input, max_new_tokens=100)[0]["generated_text"]
            if result.strip() and "Justin Timberlake" not in result:
                return result
        except Exception:
            pass

    # Fallback: Wikipedia
    try:
        return wikipedia.summary(user_input, sentences=2)
    except Exception:
        return "Sorry, I couldn’t find an answer right now."

def process_input(user_input):
    user_input = user_input.lower()
    emotion = detect_emotion(user_input)

    # 📚 Recall memory if phrase matches
    if "what is" in user_input:
        match = re.search(r"what is (.+)", user_input)
        if match:
            key = match.group(1).strip()
            value = get_fact(key)
            if value:
                return f"You told me earlier that {key} is {value}.", emotion

    # 🎭 Fun features
    if "tell me a joke" in user_input:
        return random.choice(jokes), "happy"

    if "tell me a fact" in user_input or "fun fact" in user_input:
        return random.choice(facts), "excited"

    if "who are you" in user_input:
        return "I'm your personal AI assistant — designed to grow smarter with you!", "neutral"

    if "hello" in user_input or "hi" in user_input:
        return "Hello Pradeep! How can I assist you today?", "happy"

    # 🤖 Fallback: general question answering
    response = answer_general_question(user_input)
    return response, emotion
