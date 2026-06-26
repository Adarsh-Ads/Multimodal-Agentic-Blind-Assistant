import os
import sys
import threading
import asyncio
import cv2
from PIL import Image
import customtkinter as ctk

# --- ENVIRONMENT FIX ---
# This ensures that 'src' is recognizable as a module when running gui.py directly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Now we can safely import your assistant's core logic
try:
    from src.main import run_assistant
    import src.camera as camera
except ImportError as e:
    print(f"❌ Error: Could not find the 'src' folder. Ensure gui.py is in the root directory. {e}")
    sys.exit(1)

class BlindAssistantUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Vision Assistant - Multimodal AI")
        self.geometry("900x750")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Grid Layout (3 rows: Header, Camera, Info)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Status Header
        self.status_var = ctk.StringVar(value="SYSTEM INITIALIZING...")
        self.status_label = ctk.CTkLabel(
            self, 
            textvariable=self.status_var, 
            font=("Roboto", 28, "bold"), 
            text_color="#2ecc71"
        )
        self.status_label.grid(row=0, column=0, pady=(30, 10))

        # 2. Camera Preview Frame
        # We use a black background to simulate a viewfinder
        self.video_label = ctk.CTkLabel(self, text="", fg_color="black", width=640, height=480)
        self.video_label.grid(row=1, column=0, padx=20, pady=10)

        # 3. Instruction Footer
        self.info_label = ctk.CTkLabel(
            self, 
            text="COMMANDS: HOLD [SPACEBAR] TO TALK | CTRL+SHIFT+Q TO QUIT", 
            font=("Roboto", 14, "italic"),
            text_color="#bdc3c7"
        )
        self.info_label.grid(row=2, column=0, pady=(10, 30))

        # --- INITIALIZATION ---
        # Start the backend AI loop in a daemon thread so it closes with the UI
        self.backend_thread = threading.Thread(target=self.run_backend_loop, daemon=True)
        self.backend_thread.start()
        
        # Start the video refresh loop
        self.update_video_feed()

    def run_backend_loop(self):
        """Creates a dedicated event loop for the Asyncio backend."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.status_var.set("SYSTEM READY")
            loop.run_until_complete(run_assistant())
        except Exception as e:
            print(f"❌ Backend Crash: {e}")
            self.status_var.set("BACKEND ERROR")

    def update_video_feed(self):
        """Continuously pulls frames from the persistent camera object in camera.py."""
        if camera._cap and camera._cap.isOpened():
            ret, frame = camera._cap.read()
            if ret:
                # Process frame for UI
                frame = cv2.flip(frame, 1)  # Mirror for natural feel
                cv2_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL and then to CTkImage
                pil_img = Image.fromarray(cv2_img)
                ctk_img = ctk.CTkImage(
                    light_image=pil_img, 
                    dark_image=pil_img, 
                    size=(640, 480)
                )
                
                self.video_label.configure(image=ctk_img)
        
        # 15ms delay = ~60 FPS
        self.after(15, self.update_video_feed)

if __name__ == "__main__":
    # Windows fix for multiprocessing and admin hooks
    try:
        app = BlindAssistantUI()
        app.mainloop()
    except KeyboardInterrupt:
        print("\n👋 GUI Closing...")