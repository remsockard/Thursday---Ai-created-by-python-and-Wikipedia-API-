# core/interaction_mode.py

def get_interaction_mode():
    print("👋 Welcome! How would you like to talk to me?")
    print("Type 'chat' to use text OR say 'answer my call' for voice mode.")
    
    while True:
        choice = input("➡️ Enter your choice (chat/call): ").strip().lower()
        if choice in ["chat", "text"]:
            return "chat"
        elif "call" in choice or "speak" in choice:
            return "voice"
        else:
            print("❗ Please type 'chat' or 'call'.")
