# 👁️ Multimodal Agentic Blind Assistant

A real-time, hands-free hardware simulation loop engineered to assist visually impaired users. The system synchronizes asynchronous audio capture and high-frequency video frames, passing real-time environmental context to a multimodal LLM to stream back clock-face spatial coordinates via an immediate Text-to-Speech (TTS) audio layer.

## 🏗️ Architectural Core Loop Overview

The application is structured around a continuous asynchronous execution cycle running across separate multi-threaded components:

1. Perceptual Inputs (OpenCV & PyAudio): Captures real-time physical frames via a high-definition webcam buffer and monitors raw audio signals for activation triggers.
2. Cognitive Engine (Google GenAI SDK): Utilizes the native Gemini 2.5 Flash API to process multi-layered image tensors and handle localized spatial routing analysis.
3. Audio Synthesis Layer (TTS Engine): Converted plain text coordinates back into audio frequencies instantly to provide non-visual feedback to the operator.

## 🛠️ Complete Technology Stack
- Language and Runtime: Python 3.11+
- Multimodal Processing Engine: Google GenAI Client Platform (Gemini 2.5 Flash)
- Computer Vision Capture Layer: OpenCV-Python (Matrix Frame Ingestion)
- Asynchronous Concurrency Pipeline: Asyncio Runtime & Subprocess Managers
- Presentation Interface View: Streamlit Component Framework

## 🚀 Local Deployment Execution Steps

Make sure your project virtual environment is active before initializing components.

### 1. Establish Environment Configurations
Create a .env file directly inside your repository root folder path and add your access credentials:

GEMINI_API_KEY = your_actual_google_gemini_api_token_here

### 2. Launch the Central Asynchronous Orchestrator Loop
Boot up the main routine to initialize peripheral webcam devices and launch the background tracking processes:
python src/main.py

### 3. Open the Dashboard System Interface
If viewing the diagnostic interface panel layout, activate the Streamlit frame runner:
streamlit run src/dashboard.py

Operate the device hands-free by holding down the designated hotkey trigger to capture context and receive spatial telemetry streams.