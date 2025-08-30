import re
import requests
from spellchecker import SpellChecker

from core.interaction_mode import get_interaction_mode
from voice.listen import listen_to_user
from voice.speak import speak_to_user
from core.engine import process_input
from core.math_ops import solve_math_expression, detect_math_intent
from core.emotion import update_emotion
from core.memory_core import init_memory, save_fact, get_fact
from memory import remember, recall, forget, list_memory

# === CONFIGURATION ===
spell = SpellChecker()
whitelist = {"solar", "system", "ai", "atmosphere", "earth", "html", "python", "india"}
learning_key = None
pending_lookup_key = None
AI_API_KEY = "VF.DM.6874867964978a40d4cd4e8f.EzursIEgX6rte3jC"

# === Spellchecker ===
def autocorrect(text):
    if " is " in text:
        key_part, value_part = text.split(" is ", 1)
        corrected_key = " ".join([
            word if word.lower() in whitelist else spell.correction(word)
            for word in key_part.split()
        ])
        return f"{corrected_key} is {value_part}"
    else:
        corrected = []
        for word in text.split():
            corrected_word = word if word.lower() in whitelist else spell.correction(word)
            corrected.append(corrected_word)
        return " ".join(corrected)

# === Normalization ===
def normalize_key(key):
    key = key.lower()
    key = key.replace("my ", "").replace("name", "").replace("i am", "identity").replace("i'm", "identity")
    key = key.replace("i live", "location")
    return key.strip()

# === Memory Handling ===
def process_memory_command(user_input):
    user_input = user_input.lower().strip()

    if user_input.startswith("what is my") or user_input.startswith("when is my"):
        key = normalize_key(user_input.replace("what is my", "").replace("when is my", ""))
        response = recall(key)
        update_emotion("happy" if "don't remember" not in response else "sad")
        return response

    if user_input.startswith("forget"):
        key = normalize_key(user_input.replace("forget", ""))
        if forget(key):
            update_emotion("neutral")
            return f"Okay, I forgot about {key}."
        else:
            update_emotion("confused")
            return f"I don't remember anything about {key}."

    if "what do you remember" in user_input or "list memory" in user_input:
        memory = list_memory()
        update_emotion("neutral" if memory else "sad")
        return "\n".join([f"{k.capitalize()}: {v}" for k, v in memory.items()]) if memory else "I don't remember anything yet."

    if user_input.startswith("remember ") and " is " in user_input:
        try:
            content = user_input.replace("remember", "").strip()
            key, value = content.split(" is ", 1)
            key = normalize_key(key)
            remember(key, value)
            save_fact(key, value)
            update_emotion("excited")
            return f"✔️ Got it! I’ll remember that {key} is {value}."
        except:
            update_emotion("confused")
            return "❗ Sorry, I couldn't understand what to remember."

    if " is " in user_input and user_input.startswith(("my ", "i am", "i live", "i'm")):
        try:
            key, value = user_input.split(" is ", 1)
            key = normalize_key(key)
            remember(key, value)
            save_fact(key, value)
            update_emotion("excited")
            return f"✔️ Got it! I’ll remember that {key} is {value}."
        except:
            update_emotion("confused")
            return "❗ Sorry, I couldn't understand what to remember."

    return None

# === Custom Search API ===
def ai_web_search(query):
    url = "https://api.wolframalpha.com/v1/result"
    params = {
        "i": query,
        "appid": AI_API_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None

# === Main Execution ===
def main():
    global learning_key, pending_lookup_key
    init_memory()

    speak_to_user("Hello Pradeep. I am ready to assist you.")
    print("👋 Welcome! How would you like to talk to me?")
    print("Type 'chat' to use text OR say 'answer my call' for voice mode.")

    mode = get_interaction_mode()

    while True:
        if mode == "chat":
            typed_input = input("You: ").strip().lower()
            if not typed_input:
                continue
            if "answer my call" in typed_input:
                mode = "voice"
                speak_to_user("Switching to voice mode.")
                continue
            user_input = typed_input
        else:
            user_input = listen_to_user()
            if not user_input:
                continue
            if "go to chat mode" in user_input:
                mode = "chat"
                speak_to_user("Okay, switching to chat mode.")
                continue

        user_input = autocorrect(user_input)

        if detect_math_intent(user_input):
            try:
                result = solve_math_expression(user_input)
                update_emotion("smart")
                speak_to_user(result)
            except:
                update_emotion("confused")
                speak_to_user("❌ I couldn’t solve that math expression.")
            continue

        if learning_key:
            remember(learning_key, user_input)
            save_fact(learning_key, user_input)
            update_emotion("excited")
            speak_to_user(f"✔️ Got it! I learned: {learning_key} is {user_input}.")
            learning_key = None
            continue

        memory_response = process_memory_command(user_input)
        if memory_response:
            speak_to_user(memory_response)
            continue

        if pending_lookup_key:
            if "search" in user_input:
                result = ai_web_search(pending_lookup_key)
                if result:
                    remember(pending_lookup_key, result)
                    save_fact(pending_lookup_key, result)
                    update_emotion("relieved")
                    speak_to_user(f"🌐 {result}")
                else:
                    speak_to_user("❌ Couldn't find anything useful online.")
                pending_lookup_key = None
                continue
            elif "learn" in user_input or "teach" in user_input:
                learning_key = pending_lookup_key
                pending_lookup_key = None
                speak_to_user(f"🧠 Great! Tell me what {learning_key} is.")
                continue

        match = re.search(r"(?:what|when|who) is (.+)", user_input)
        if match:
            key = match.group(1).strip()
            value = get_fact(key)
            if value:
                update_emotion("happy")
                speak_to_user(f"🧠 You told me earlier: {key} is {value}.")
            else:
                pending_lookup_key = key
                update_emotion("curious")
                speak_to_user("🤔 I don’t know that yet. Would you like to *teach* me or should I *search* it online?")
            continue

        if any(x in user_input for x in ["exit", "quit", "bye", "stop"]):
            update_emotion("neutral")
            speak_to_user("Goodbye Pradeep. Shutting down. See you soon.")
            break

        response, emotion = process_input(user_input)
        update_emotion(emotion)
        speak_to_user(response)

# === UI Thread ===
def process_user_input(text):
    global learning_key, pending_lookup_key
    text = autocorrect(text)

    if detect_math_intent(text):
        update_emotion("smart")
        return solve_math_expression(text), "smart"

    memory_response = process_memory_command(text)
    if memory_response:
        return memory_response, "neutral"

    if learning_key:
        remember(learning_key, text)
        save_fact(learning_key, text)
        learning_key = None
        update_emotion("excited")
        return f"✔️ Got it! I learned: {learning_key} is {text}.", "excited"

    if pending_lookup_key:
        if "learn" in text or "teach" in text:
            learning_key = pending_lookup_key
            pending_lookup_key = None
            return f"🧠 Great! Tell me what {learning_key} is.", "curious"
        elif "search" in text:
            result = ai_web_search(pending_lookup_key)
            if result:
                remember(pending_lookup_key, result)
                save_fact(pending_lookup_key, result)
                pending_lookup_key = None
                update_emotion("relieved")
                return f"🌐 {result}", "relieved"
            else:
                pending_lookup_key = None
                return "❌ Couldn't find anything online.", "sad"

    match = re.search(r"(?:what|when|who) is (.+)", text)
    if match:
        key = match.group(1).strip()
        value = get_fact(key)
        if value:
            update_emotion("happy")
            return f"🧠 You told me earlier: {key} is {value}.", "happy"
        pending_lookup_key = key
        update_emotion("curious")
        return "🤔 I don’t know that yet. Would you like to *teach* me or should I *search* it online?", "curious"

    response, emotion = process_input(text)
    update_emotion(emotion)
    return response, emotion

if __name__ == "__main__":
    main()
