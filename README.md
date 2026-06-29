# 👁️ Multimodal Agentic Blind Assistant

A real-time, hands-free hardware simulation loop engineered to assist visually impaired users. The system synchronizes asynchronous audio capture and high-frequency video frames, passing real-time environmental context to a multimodal LLM to stream back clock-face spatial coordinates via an immediate Text-to-Speech (TTS) audio layer.

## 🏗️ Architectural Core Loop Overview

The application is structured around a continuous asynchronous execution cycle running across separate multi-threaded components:

1. Perceptual Inputs (OpenCV & PyAudio): Captures real-time physical frames via a high-definition webcam buffer and monitors raw audio signals for activation triggers.
2. Cognitive Engine (Google GenAI SDK): Utilizes the native Gemini 3 Flash API to process multi-layered image tensors and handle localized spatial routing analysis.
3. Audio Synthesis Layer (RealtimeTTS Engine): Converts plain text coordinates back into audio frequencies instantly to provide zero-latency voice feedback to the operator using neural streaming voice channels.

## 🛠️ Complete Technology Stack
- Language and Runtime: Python 3.11+
- Multimodal Processing Engine: Google GenAI Client Platform (Gemini-3-Flash-Preview)
- Automatic Speech Recognition Engine: Faster-Whisper-Tiny (Int8 CPU Quantized)
- Real-Time Audio Synthesis Module: RealtimeTTS with Neural Microsoft Edge Core
- Computer Vision Capture Layer: OpenCV-Python (Matrix Frame Ingestion)
- Asynchronous Concurrency Pipeline: Asyncio Runtime Execution Framework
- Presentation Interface System: CustomTkinter Core UI & Streamlit Viewfinder Panel

## 🚀 Local Deployment Execution Steps

Ensure your project virtual environment is active before initializing components.

### 1. Establish Environment Configurations
Create a .env file directly inside your repository root folder path and add your access credentials:

GEMINI_API_KEY = your_actual_google_gemini_api_token_here

### 2. Launch the Central Asynchronous Orchestrator Loop (Terminal Option 1)
Boot up the main system loop configuration to run directly inside your console shell terminal:
python src/main.py

### 3. Initialize the CustomTkinter Native Desktop Control Board (Terminal Option 2)
To access the full hardware simulation desktop control dashboard view, execute:
python gui.py

### 4. Open the Web Viewfinder Diagnostic Interface Panel (Terminal Option 3)
If monitoring state arrays through a browser layout, launch the Streamlit server wrapper:
streamlit run app.py

Operate the device hands-free by holding down the designated [SPACEBAR] key to pass context and receive immediate spatial voice streams.