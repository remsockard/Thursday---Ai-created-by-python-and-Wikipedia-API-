# core/intent.py

def detect_intent(user_input):
    user_input = user_input.lower()

    if "remember" in user_input and " is " in user_input:
        return "save_memory"
    
    elif "what is" in user_input:
        return "recall_memory"

    elif any(word in user_input for word in ["exit", "quit", "goodbye", "stop"]):
        return "exit"

    elif any(word in user_input for word in ["thank", "wrong", "sad", "lonely", "excited", "happy"]):
        return "emotion_trigger"

    elif any(word in user_input for word in ["hi", "hello", "hey"]):
        return "greeting"

    elif any(word in user_input for word in ["open file", "show file", "delete file"]):
        return "file_command"

    elif "joke" in user_input:
        return "fun_request"

    else:
        return "general_question"
