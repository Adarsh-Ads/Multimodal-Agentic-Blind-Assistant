import asyncio
import re
import os
import sys
from RealtimeTTS import TextToAudioStream, EdgeEngine

# Inject local pre-compiled binaries into systems path vector environmental arrays
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bin_path = os.path.join(project_root, "bin")

if os.path.exists(bin_path):
    os.environ["PATH"] += os.pathsep + bin_path
    print(f"🔗 External binary library linkages configured: {bin_path}")

try:
    engine = EdgeEngine()
    engine.set_voice("en-US-AvaMultilingualNeural")
    print("✅ High-Fidelity EdgeEngine Voice Layer Successfully Configured.")
except Exception as e:
    print(f"❌ Cloud Synthesis Driver Ingestion Fault: {e}")
    try:
        from RealtimeTTS import SystemEngine
        engine = SystemEngine()
        print("⚠️ Falling back to native offline system synthesizer engine.")
    except Exception:
        engine = None
        print("🛑 Critical: No compatible text synthesis engine found.")

stream = TextToAudioStream(engine) if engine else None

def feed_audio(chunk):
    """
    Applies aggressive regular expression sanitization masks to incoming tokens
    to slice off rogue markdown fragments and prevent speech disruption loops.
    """
    if stream and chunk:
        clean_chunk = re.sub(r'[\*\-\#\`]', '', chunk)
        clean_chunk = " ".join(clean_chunk.split())
        
        if clean_chunk.strip():
            stream.feed(clean_chunk)

def start_audio_stream():
    """
    Triggers concurrent, asynchronous chunk synthesis streaming via unblocked
    background player tasks prior to model execution completion.
    """
    if stream and not stream.is_playing():
        stream.play_async(
            fast_sentence_fragment=True,
            buffer_threshold_seconds=0.1
        )

def stop_audio():
    """Abruptly flushes active buffer arrays to force stop ongoing speech tracks."""
    if stream:
        stream.stop()

async def speak_stream_finish():
    """
    Offloads blockable synchronous playback queues onto separate multi-threaded execution pools,
    preventing frame capture and event loop locking scenarios.
    """
    if stream:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, stream.play)