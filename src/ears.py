from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import keyboard

FS = 16000  
CHUNK_SIZE = 1024 

print("Loading optimized Whisper Quantized Automatic Speech Recognition Engine...")
model = WhisperModel("tiny", device="cpu", compute_type="int8")

def listen_until_release():
    """
    Polls keyboard device drivers to handle dynamic Push-to-Talk execution loops,
    streams audio input into memory buffers, and outputs a normalized text transcription vector.
    """
    print("🎤 Opening audio peripheral channel stream...")
    recording = []
    
    try:
        with sd.InputStream(samplerate=FS, channels=1, dtype='float32', blocksize=CHUNK_SIZE) as stream:
            while keyboard.is_pressed(' '):
                chunk, overflowed = stream.read(CHUNK_SIZE)
                if not overflowed:
                    recording.append(chunk.copy())
                    
    except Exception as e:
        print(f"❌ Structural Audio Component Fault: {e}")
        return ""

    if not recording:
        return ""

    # Processing spatial matrix blocks into normalized single-channel PCM vectors
    full_audio = np.concatenate(recording, axis=0)
    if not os.path.exists('data'): 
        os.makedirs('data')
    wav_path = "data/input.wav"
    wav.write(wav_path, FS, (full_audio * 32767).astype(np.int16))
    
    # Beam-size configuration set to 1 to optimize for near-zero operational latencies
    segments, _ = model.transcribe(wav_path, beam_size=1, language='en')
    text = " ".join([segment.text for segment in segments]).strip()
    
    return text if len(text) > 1 else ""