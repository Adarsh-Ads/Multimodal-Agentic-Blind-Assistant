from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import keyboard

FS = 16000  
CHUNK_SIZE = 1024 

# Pre-load model into memory
print("Loading Whisper model (tiny, int8)...")
model = WhisperModel("tiny", device="cpu", compute_type="int8")

def listen_until_release():
    """Records audio only as long as the spacebar is held down."""
    print("🎤 Listening...")
    recording = []
    
    try:
        with sd.InputStream(samplerate=FS, channels=1, dtype='float32', blocksize=CHUNK_SIZE) as stream:
            while keyboard.is_pressed(' '):
                chunk, overflowed = stream.read(CHUNK_SIZE)
                if not overflowed:
                    recording.append(chunk.copy())
                    
    except Exception as e:
        print(f"❌ Audio Hardware Error: {e}")
        return ""

    if not recording:
        return ""

    full_audio = np.concatenate(recording, axis=0)
    if not os.path.exists('data'): os.makedirs('data')
    wav_path = "data/input.wav"
    wav.write(wav_path, FS, (full_audio * 32767).astype(np.int16))
    
    # Transcribe with beam_size 1 for maximum speed
    segments, _ = model.transcribe(wav_path, beam_size=1, language='en')
    text = " ".join([segment.text for segment in segments]).strip()
    
    return text if len(text) > 1 else ""