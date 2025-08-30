import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import threading
import requests
from main import process_user_input  # ✅ AI logic
from core.emotion import update_emotion

# === CONFIGURATION ===
EMOTION_FOLDER = "assets/emotions"
MASCOT_SIZE = (100, 100)

class AIAssistantUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mascot Assistant")
        self.root.geometry("360x480+100+100")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # === Main Container (Now grey with no outer black padding) ===
        self.container = tk.Frame(self.root, bg="#e0e0e0", bd=0, highlightthickness=2, highlightbackground="gray")
        self.container.pack(expand=True, fill="both")
        self.container.bind('<B1-Motion>', self.move_window)
        self.container.bind('<Button-1>', self.get_pos)

        # === Mascot Image ===
        self.mascot_img_label = tk.Label(self.container, bg="#e0e0e0")
        self.mascot_img_label.pack(pady=(8, 4))
        self.update_mascot("neutral")

        # === Chat Display ===
        self.chat_display = tk.Text(self.container, height=10, wrap="word", bg="#f4f4f4", fg="black", bd=1, relief="flat")
        self.chat_display.pack(padx=10, pady=(0, 4), fill="both", expand=True)
        self.chat_display.config(state="disabled")

        # === Input Frame ===
        input_frame = tk.Frame(self.container, bg="#e0e0e0")
        input_frame.pack(padx=10, pady=4, fill="x")

        self.input_box = tk.Entry(input_frame, bg="white", fg="black", font=("Segoe UI", 10), relief="solid", bd=1)
        self.input_box.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.input_box.bind("<Return>", self.send_input)

        send_btn = tk.Button(input_frame, text="Send", command=self.send_input, bg="#0078D7", fg="white", relief="flat")
        send_btn.pack(side="right")

        attach_btn = tk.Button(self.container, text="📎 Attach", command=self.attach_file, bg="#E0E0E0", relief="flat")
        attach_btn.pack(pady=(0, 5))

        self.display_message("AI", "👋 Hello Pradeep! I'm ready to chat or answer your call.")

    def update_mascot(self, emotion):
        path = os.path.join(EMOTION_FOLDER, f"{emotion}.png")
        if not os.path.exists(path):
            path = os.path.join(EMOTION_FOLDER, "neutral.png")
        img = Image.open(path).resize(MASCOT_SIZE)
        photo = ImageTk.PhotoImage(img)
        self.mascot_img_label.configure(image=photo)
        self.mascot_img_label.image = photo

    def display_message(self, sender, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"{sender}: {message}\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def send_input(self, event=None):
        user_text = self.input_box.get().strip()
        if not user_text:
            return
        self.display_message("You", user_text)
        self.input_box.delete(0, tk.END)
        threading.Thread(target=self.process_ai_response, args=(user_text,), daemon=True).start()

    def process_ai_response(self, text):
        try:
            response, emotion = process_user_input(text)
            update_emotion(emotion)
            self.display_message("AI", response)
            self.update_mascot(emotion)
        except Exception as e:
            self.display_message("AI", f"[Error] {str(e)}")

    def attach_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.display_message("You", f"📎 Attached: {os.path.basename(file_path)}")

    def get_pos(self, event):
        self.xwin = event.x
        self.ywin = event.y

    def move_window(self, event):
        self.root.geometry(f'+{event.x_root - self.xwin}+{event.y_root - self.ywin}')

# ==== Run App ====
def run_ui():
    root = tk.Tk()
    app = AIAssistantUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_ui()
