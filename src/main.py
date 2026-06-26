import asyncio
import keyboard
from src.camera import capture_image
from src.ears import listen_until_release # Updated function
from src.brain import init_chat, analyze_scene_stream_chat 
from src.voice import feed_audio, stop_audio, speak_stream_finish, start_audio_stream
from src.sounds import play_success_chime, play_error_chime, play_stop_chime

speaking_task = None
stop_event = asyncio.Event()

async def run_assistant():
    global speaking_task
    print("🚀 System Ready.")
    print("👉 HOLD SPACEBAR to talk. RELEASE to process.")
    
    await init_chat()
    start_audio_stream()
    feed_audio("System online.")
    await speak_stream_finish()
    
    loop = asyncio.get_running_loop()
    
    while not stop_event.is_set():
        # 1. Check for Emergency Quit
        if keyboard.is_pressed('ctrl+shift+q'):
            play_stop_chime()
            stop_event.set()
            break
            
        # 2. Check for Push to Talk
        if keyboard.is_pressed(' '):
            # Instant Interrupt if AI is already talking
            if speaking_task and not speaking_task.done():
                speaking_task.cancel()
                stop_audio()
                print("\n🛑 Interrupting...")

            # Record while key is held
            query = await loop.run_in_executor(None, listen_until_release)
            
            if query:
                print(f"🗨️ User: {query}")
                play_success_chime()
                img_path = capture_image()
                speaking_task = asyncio.create_task(process_and_speak(img_path, query))
            else:
                play_error_chime()

        await asyncio.sleep(0.05) # Small sleep for CPU efficiency

async def process_and_speak(img_path, query):
    print("🤖 Response: ", end="", flush=True)
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
        print(f"\nError: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_assistant())
    finally:
        print("🛑 Assistant stopped.")