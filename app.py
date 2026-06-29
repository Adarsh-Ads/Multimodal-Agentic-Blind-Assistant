import streamlit as st
import os
import sys
import threading
import asyncio
import cv2
import time
from PIL import Image

# Enforce permanent top-level root module paths to keep dynamic directory resolution working seamlessly
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

try:
    from src.main import run_assistant
    import src.camera as camera
except ModuleNotFoundError as e:
    st.error(f"Module Resolution Fault: {e}. Execute component from project root folder workspace path.")
    st.stop()

st.set_page_config(
    page_title="VisionEye Assistant",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stHeader { color: #2ecc71; }
    .status-indicator {
        padding: 10px;
        border-radius: 8px;
        border-left: 5px solid #2ecc71;
        background-color: #1e2130;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'backend_running' not in st.session_state:
    st.session_state.backend_running = False

def start_backend():
    """Initializes and runs the core async task event driver framework safely in an isolated sub-thread worker."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_assistant())
    except Exception as e:
        print(f"Background worker execution fail: {e}")

if not st.session_state.backend_running:
    thread = threading.Thread(target=start_backend, daemon=True)
    thread.start()
    st.session_state.backend_running = True

st.title("👁️ VisionEye Assistant")
st.markdown("### Multimodal AI for the Visually Impaired")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Live Viewfinder")
    video_placeholder = st.empty()

with col_right:
    st.subheader("System Control")
    st.markdown('<div class="status-indicator">🟢 AI ENGINE: ACTIVE</div>', unsafe_allow_html=True)
    st.info("**Push-to-Talk Command:** Hold down the global **[SPACEBAR]** device macro key.")
    
    with st.expander("System Architecture Blueprint Specs", expanded=True):
        st.write("**Core Inference Framework:** Gemini-3-Flash")
        st.write("**Speech-to-Text Translation Layer:** Faster-Whisper (Tiny)")
        st.write("**Text-to-Speech Synthesis:** Edge-Neural (Ava)")
    
    if st.button("🔄 Reset Camera Feed"):
        if camera._cap:
            camera._cap.release()
            camera._cap = None
        st.rerun()

# Dynamic multi-threaded display processing pipeline loop
try:
    while True:
        if camera._cap and camera._cap.isOpened():
            ret, frame = camera._cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video_placeholder.image(frame_rgb, use_container_width=True)
        time.sleep(0.02)
except Exception as e:
    print(f"Diagnostic dashboard framing engine drop out: {e}")