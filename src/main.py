import asyncio
import keyboard
from src.camera import capture_image
from src.ears import listen_until_release 
from src.brain import init_chat, analyze_scene_stream_chat 
from src.voice import feed_audio, stop_audio, speak_stream_finish, start_audio_stream
from src.sounds import play_success_chime, play_error_chime, play_stop_chime

speaking_task = None
stop_event = asyncio.Event()

async def run_assistant():
    """
    Main asynchronous pipeline tracking kernel state events, managing keyboard macro intercepts,
    and matching resource scheduling allocations elegantly without lock deadlocks.
    """
    global speaking_task
    print("🚀 System Orchestrator Core Active.")
    print("👉 HOLD [SPACEBAR] to prompt. RELEASE to pass multi-layered contextual arrays.")
    
    await init_chat()
    start_audio_stream()
    feed_audio("System online.")
    await speak_stream_finish()
    
    loop = asyncio.get_running_loop()
    
    while not stop_event.is_set():
        if keyboard.is_pressed('ctrl+shift+q'):
            play_stop_chime()
            stop_event.set()
            break
            
        if keyboard.is_pressed(' '):
            # Premature interruption mechanism: instantly breaks talking tasks if new request fires
            if speaking_task and not speaking_task.done():
                speaking_task.cancel()
                stop_audio()
                print("\n🛑 Pipeline task cancel command received. Interrupted speech path.")

            # Processing intensive synchronous hardware polling via a thread executor block
            query = await loop.run_in_executor(None, listen_until_release)
            
            if query:
                print(f"🗨️ User Intent Token: {query}")
                play_success_chime()
                img_path = capture_image()
                speaking_task = asyncio.create_task(process_and_speak(img_path, query))
            else:
                play_error_chime()

        # Dynamic sleep injection prevents execution kernel thread saturation
        await asyncio.sleep(0.05) 

async def process_and_speak(img_path, query):
    """Encapsulates the context tracking and asynchronous text generation pipeline."""
    print("🤖 Processing Response: ", end="", flush=True)
    try:
        start_audio_stream()
        async for chunk in analyze_scene_stream_chat(img_path, query):
            print(chunk, end="", flush=True)
            feed_audio(chunk)
        await speak_stream_finish()
        print() 
    except asyncio.CancelledError:
        stop_audio()
    except Exception as e:
        print(f"\nProcessing exception pipeline drop: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_assistant())
    finally:
        print("🛑 System components gracefully uncoupled. Process stopped.")