import tkinter as tk
from PIL import Image, ImageTk
import os

from main import process_user_input  # ✅ Use real AI logic

# === CONFIG ===
MASCOT_SIZE = (256, 256)
EMOTION_FOLDER = "assets/emotions"
DEFAULT_EMOTION = "neutral"

class MascotChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mascot AI")
        self.root.geometry("360x520+100+100")
        self.root.configure(bg="white")
        self.root.overrideredirect(True)  # ✅ Frameless
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")  # ✅ Invisible edges

        # === Draggable Area (Top 24px)
        self.drag_area = tk.Frame(self.root, bg="white", height=24)
        self.drag_area.pack(fill="x")
        self.drag_area.bind("<Button-1>", self.save_last_click_pos)
        self.drag_area.bind("<B1-Motion>", self.move_window)

        # === Mascot Image ===
        self.image_label = tk.Label(self.root, bg="white")
        self.image_label.pack()
        self.update_emotion_image(DEFAULT_EMOTION)

        # === Chat Display ===
        self.chat_box = tk.Text(self.root, height=10, wrap="word", bg="#f7f7f7", fg="#000", bd=0)
        self.chat_box.pack(padx=10, pady=(4, 0), fill="both", expand=True)
        self.chat_box.config(state="disabled")

        # === Input Box ===
        self.entry = tk.Entry(self.root, bd=0, bg="#e0e0e0", font=("Segoe UI", 10))
        self.entry.pack(padx=10, pady=(0, 5), fill="x")
        self.entry.bind("<Return>", self.send_message)

        # === Optional Close on Double Click Top Left ===
        self.drag_area.bind("<Double-Button-1>", lambda e: self.root.destroy())

        # === Initial Greeting ===
        self.display_message("AI", "👋 Hello Pradeep! I'm ready to assist you.")

    def update_emotion_image(self, emotion):
        path = os.path.join(EMOTION_FOLDER, f"{emotion}.png")
        if not os.path.exists(path):
            path = os.path.join(EMOTION_FOLDER, "neutral.png")
        image = Image.open(path).resize(MASCOT_SIZE)
        self.mascot_photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.mascot_photo)

    def display_message(self, sender, message):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, f"{sender}: {message}\n")
        self.chat_box.config(state="disabled")
        self.chat_box.see("end")

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.entry.delete(0, tk.END)
        self.display_message("You", user_input)

        try:
            reply, emotion = process_user_input(user_input)
            self.display_message("AI", reply)
            self.update_emotion_image(emotion)
        except Exception as e:
            self.display_message("AI", f"[Error] {str(e)}")
            self.update_emotion_image("confused")

    def save_last_click_pos(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def move_window(self, event):
        x = event.x_root - self.x_offset
        y = event.y_root - self.y_offset
        self.root.geometry(f"+{x}+{y}")

# === RUN ===
def launch_mascot():
    root = tk.Tk()
    app = MascotChatUI(root)
    root.mainloop()

if __name__ == "__main__":
    launch_mascot()
