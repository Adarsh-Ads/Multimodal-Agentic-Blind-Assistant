# 👁️ VisionEye Assistant — User Setup & Operation Guide

Welcome to the **VisionEye Assistant**, a real-time, voice-controlled AI companion designed to help visually impaired individuals navigate their surroundings safely. 

By holding down your keyboard's **Spacebar**, the assistant listens to your voice question, takes a localized picture using your webcam, and reads back a clear, safety-prioritized description of what is ahead of you using a natural neural voice.

---

## 🛠️ System Requirements

Before configuring the software, please ensure your system meets these prerequisites:

1. **Operating System:** Optimized for Windows 10 / 11.
2. **Hardware:** A functional **Webcam** and a **Microphone** must be connected to your system.
3. **Media Engine Dependency (mpv):**
   * The text-to-speech engine requires the external player files `mpv.exe` and `libmpv-2.dll` to be placed directly inside the `bin` folder of this project directory.
   * If configuring on Linux or macOS, install `mpv` globally via your package manager:
     * Ubuntu/Debian: `sudo apt update && sudo apt install mpv libmpv-dev`
     * macOS: `brew install mpv`

---

## 📦 How to Set Up the Assistant

Follow these step-by-step instructions to configure the application workspace:

1. **Download and Open the Project:**
   Extract or download the assistant project folder to your local machine and open your system terminal or command prompt inside it.

2. **Isolate Python Dependencies:**
   Create and activate an isolated virtual runtime environment to prevent system package version conflicts by running:
   
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On Linux/macOS:
   source venv/bin/activate

3. **Install Core Requirements:**
   Run the following command to download and install all the underlying interface libraries:
   
   pip install --upgrade pip
   pip install -r requirements.txt

4. **Add Your Gemini AI Access Key:**
   The assistant requires a valid Google Gemini API connection to analyze scenes.
   * Generate a file named `.env` in the root folder using the `.env.example` file as a reference.
   * Open the `.env` file using a standard text editor (like Notepad) and add your key:
     GEMINI_API_KEY=your_actual_gemini_api_key_here

---

## 🎮 How to Launch and Run the Assistant

You can launch the system using either a standalone desktop app or a web-based layout:

### Option A: Launching the Desktop Application (Recommended)
This brings up an ultra-responsive desktop window built with CustomTkinter:
python gui.py

### Option B: Launching the Web Dashboard Interface
This opens a modern visual dashboard matrix inside your web browser:
streamlit run app.py

---

## ⌨️ Universal Control Guide

Because the application uses global keyboard listeners, these inputs work even if the application window is minimized or running in the background:

| Command Input | System Feedback Action |
| :--- | :--- |
| 🎤 HOLD SPACEBAR | Activates your microphone and tracks your voice query continuously. |
| 🚀 RELEASE SPACEBAR | Captures a webcam image frame, runs the AI model, and streams the verbal description back immediately. |
| 🛑 PRESS SPACEBAR AGAIN | Instant Interrupt: Instantly cancels active text-to-speech output, flushes buffers, and prepares for a new query. |
| ❌ CTRL + SHIFT + Q | Emergency Quit: Disconnects background camera threads, closes audio channels, and safely shuts down the application. |

---

## 🧠 Core Operational Design Rules

When interacting with the assistant, it strictly executes under these safety and accessibility parameters:

* **Clean Conversational Output:** The software dynamically filters out formatting text, asterisks (*), lines, or markdown notation before feeding the chunks to the audio stream, ensuring fluid speech delivery.
* **The "Clock Face" Spatial Convention:** Relative positions of physical items are always mapped to an analog clock layout. Items straight ahead are at 12 o'clock, objects to your direct right are at 3 o'clock, and anything behind you is at 6 o'clock.
* **Safety-First Warnings:** If an immediate environmental hazard is encountered (e.g., a tripping hazard, an open edge, or a low-hanging item), the system announces that hazard at the absolute beginning of its phrase before clarifying any background ambient features.
