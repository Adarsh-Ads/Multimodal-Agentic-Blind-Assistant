import streamlit as st
import os
import sys
import threading
import asyncio
import cv2
import time
from PIL import Image

# ==========================================
# PERMANENT PATH FIX (Must be before src imports)
# ==========================================
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import backend components
try:
    from src.main import run_assistant
    import src.camera as camera
except ModuleNotFoundError as e:
    st.error(f"Module Discovery Error: {e}. Ensure you are running from the root directory.")
    st.stop()

# ==========================================
# STREAMLIT UI CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="VisionEye Assistant",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Professional Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stHeader { color: #2ecc71; }
    .reportview-container { background: #0e1117; }
    .status-indicator {
        padding: 10px;
        border-radius: 8px;
        border-left: 5px solid #2ecc71;
        background-color: #1e2130;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# BACKEND ORCHESTRATION
# ==========================================
if 'backend_running' not in st.session_state:
    st.session_state.backend_running = False

def start_backend():
    """Runs the main assistant loop in a persistent background thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_assistant())
    except Exception as e:
        print(f"Backend Thread Error: {e}")

# Start backend once
if not st.session_state.backend_running:
    thread = threading.Thread(target=start_backend, daemon=True)
    thread.start()
    st.session_state.backend_running = True

# ==========================================
# MAIN UI LAYOUT
# ==========================================
st.title("👁️ VisionEye Assistant")
st.markdown("### Multimodal AI for the Visually Impaired")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Live Viewfinder")
    # Placeholder for the live OpenCV stream
    video_placeholder = st.empty()

with col_right:
    st.subheader("System Control")
    st.markdown('<div class="status-indicator">🟢 AI ENGINE: ACTIVE</div>', unsafe_allow_html=True)
    
    st.info("**Push-to-Talk:** Hold the **[SPACEBAR]** on your keyboard.")
    
    with st.expander("System Specs", expanded=True):
        st.write("**Model:** Gemini-3-Flash")
        st.write("**STT:** Faster-Whisper (Tiny)")
        st.write("**TTS:** Edge-Neural (Ava)")
    
    if st.button("🔄 Reset Camera Feed"):
        if camera._cap:
            camera._cap.release()
            camera._cap = None
        st.rerun()

# ==========================================
# LIVE FEED REFRESH LOOP
# ==========================================
try:
    while True:
        if camera._cap and camera._cap.isOpened():
            ret, frame = camera._cap.read()
            if ret:
                # Process for UI: Mirror and Convert Colors
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Update the Streamlit placeholder with the new image
                video_placeholder.image(frame_rgb, use_container_width=True)
        
        # Small sleep to prevent high CPU usage while maintaining fluid FPS
        time.sleep(0.02)
except Exception as e:
    print(f"UI Stream Error: {e}")