import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Global variable to persist session
chat_session = None

def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def init_chat():
    global chat_session
    client = get_client()
    
    print("Initializing new chat session...")
    config = types.GenerateContentConfig(
        system_instruction=(
            "You are an expert multimodal personal assistant for a blind user. "
            "You are an assistant for the blind. IMPORTANT: Do not use any markdown formatting, bullet points, or asterisks. Write in plain, conversational paragraphs only. Never use symbols like '*' or '-' at the start of lines."
            "Always use the 'Clock Face' method to describe relative positions "
            "(e.g., 'The door is at 2 o'clock'). "
            "Maintain context of previous objects identified in this session."
            "When reporting on safety, always state the most critical immediate hazard first (e.g., 'Warning: tripping hazard at 7 o'clock'). Do not wait for a full analysis to give the most important warning."
            """STRICT RULES FOR VOICE OUTPUT:
                1. NEVER use asterisks (*), bullet points, dashes (-), or hashtags (#).
                2. NEVER use markdown formatting of any kind.
                3. Use plain, conversational English sentences only.
                4. Use the 'Clock Face' method for all object locations (e.g., 'A chair is at 2 o'clock').
                5. Prioritize immediate hazards (tripping risks, open doors, sharp corners).
                6. Be concise. Do not describe the user's clothing unless they ask.
            Example: 'Directly ahead of you at 12 o'clock is a wooden table. To your left at 9 o'clock, there is a low-hanging plant. The floor is clear.'"""
        ),
        thinking_config=types.ThinkingConfig(thinking_level="minimal")
    )
    
    # Explicitly set the global variable
    chat_session = client.aio.chats.create(
        model="gemini-3-flash-preview",
        config=config
    )
    print("Chat session initialized successfully.")

async def analyze_scene_stream_chat(image_path, user_query):
    global chat_session
    
    # Ensure chat is initialized
    if chat_session is None:
        await init_chat()
    
    print(f"DEBUG: Using Chat Session: {chat_session is not None}")

    try:
        # Prepare image bytes
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        
        image_part = types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')
        
        # Send message to the session
        response_stream = await chat_session.send_message_stream([user_query, image_part])
        
        async for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"Error: {str(e)}"