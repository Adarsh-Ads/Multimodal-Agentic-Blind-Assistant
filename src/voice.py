import asyncio
import re
import os
import sys
from RealtimeTTS import TextToAudioStream, EdgeEngine

# --- Path Configuration for MPV ---
# Ensures RealtimeTTS finds the mpv.exe in your local bin folder
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bin_path = os.path.join(project_root, "bin")

if os.path.exists(bin_path):
    os.environ["PATH"] += os.pathsep + bin_path
    print(f"🔗 Linked local binaries at: {bin_path}")

# --- Engine Configuration ---
try:
    # Initialize EdgeEngine (Microsoft Neural Voices)
    engine = EdgeEngine()
    
    # Using 'en-US-AvaMultilingualNeural' for a modern, friendly human tone
    # Alternatives: 'en-IN-NeerjaNeural' or 'en-US-AndrewMultilingualNeural'
    engine.set_voice("en-US-AvaMultilingualNeural")
    
    print("✅ EdgeEngine Activated: Using Natural Neural Voice")
except Exception as e:
    print(f"❌ EdgeEngine failed: {e}")
    try:
        from RealtimeTTS import SystemEngine
        engine = SystemEngine()
        print("⚠️ Falling back to SystemEngine (Offline)")
    except Exception:
        engine = None
        print("🛑 No Audio Engine available.")

# --- Stream Initialization ---
# We keep the constructor simple to avoid TypeError across different versions
stream = TextToAudioStream(engine) if engine else None

def feed_audio(chunk):
    """Feeds text into the buffer with markdown stripping."""
    if stream and chunk:
        # Strip markdown noise: asterisks, hashes, dashes, and backticks
        clean_chunk = re.sub(r'[\*\-\#\`]', '', chunk)
        
        # Clean up whitespace
        clean_chunk = " ".join(clean_chunk.split())
        
        if clean_chunk.strip():
            stream.feed(clean_chunk)

def start_audio_stream():
    """Starts the background playback thread with zero-latency flags."""
    if stream and not stream.is_playing():
        # fast_sentence_fragment: Starts audio before the AI finishes the sentence
        # buffer_threshold_seconds: Reduces the 'wait time' for enough text to speak
        stream.play_async(
            fast_sentence_fragment=True,
            buffer_threshold_seconds=0.1
        )

def stop_audio():
    """Immediately stops and clears the audio buffer."""
    if stream:
        stream.stop()

async def speak_stream_finish():
    """Ensures the remaining buffer is played before the next capture."""
    if stream:
        # Run the synchronous stream.play() in a thread to keep the event loop alive
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, stream.play)