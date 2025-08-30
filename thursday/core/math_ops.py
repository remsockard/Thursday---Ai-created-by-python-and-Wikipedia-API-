# core/math_ops.py

def solve_math_expression(expression):
    """
    Evaluate a math expression safely and return the result.
    Supported operations: +, -, *, /, %, **, (), etc.
    """
    try:
        # Remove unsafe characters
        expression = expression.replace("^", "**")
        allowed_chars = "0123456789+-*/%.() "
        if not all(char in allowed_chars for char in expression):
            return "❌ Invalid characters in expression."

        # Evaluate
        result = eval(expression, {"__builtins__": None}, {})
        return f"🧮 The answer is: {result}"
    except ZeroDivisionError:
        return "⚠️ You can't divide by zero."
    except Exception:
        return "❌ I couldn't understand that math expression."


def detect_math_intent(user_input):
    """
    Detect if the user input looks like a math problem.
    """
    import re
    pattern = r"[0-9]+\s*[-+*/%^()]\s*[0-9]+"
    return bool(re.search(pattern, user_input))
