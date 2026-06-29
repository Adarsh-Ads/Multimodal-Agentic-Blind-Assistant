import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Establish deterministic paths to resolve environmental configuration vectors
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Stateful Singleton instance to persist conversation context across sequential frames
chat_session = None

def get_client():
    """Instantiates and returns an authenticated Google GenAI platform client pipeline."""
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def init_chat():
    """
    Asynchronously builds the persistent conversation engine, injecting systemic instructions
    to eliminate markdown formatting and enforce structural spatial orientation standards.
    """
    global chat_session
    client = get_client()
    
    print("Initializing long-lived stateful multimodal chat container...")
    config = types.GenerateContentConfig(
        system_instruction=(
            "You are an expert multimodal personal assistant for a blind user. "
            "IMPORTANT: Do not use any markdown formatting, bullet points, or asterisks. "
            "Write in plain, conversational paragraphs only. Never use symbols like '*' or '-' at the start of lines. "
            "Always use the 'Clock Face' method to describe relative positions (e.g., 'The door is at 2 o'clock'). "
            "Maintain context of previous objects identified in this session. "
            "When reporting on safety, always state the most critical immediate hazard first. "
            "STRICT RULES FOR VOICE OUTPUT:\n"
            "1. NEVER use asterisks (*), bullet points, dashes (-), or hashtags (#).\n"
            "2. NEVER use markdown formatting of any kind.\n"
            "3. Use plain, conversational English sentences only.\n"
            "4. Use the 'Clock Face' method for all object locations.\n"
            "5. Prioritize immediate hazards first.\n"
            "6. Be concise. Do not describe clothing unless explicitly asked."
        ),
        thinking_config=types.ThinkingConfig(thinking_level="minimal")
    )
    
    chat_session = client.aio.chats.create(
        model="gemini-3-flash-preview",
        config=config
    )
    print("Multimodal session container successfully established.")

async def analyze_scene_stream_chat(image_path, user_query):
    """
    Ingests a localized image asset, wraps it inside an ephemeral binary token byte part,
    and yields streaming asynchronous text tokens back to the main thread core.
    """
    global chat_session
    
    if chat_session is None:
        await init_chat()
    
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        
        image_part = types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')
        response_stream = await chat_session.send_message_stream([user_query, image_part])
        
        async for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"Inference pipeline execution error: {str(e)}"