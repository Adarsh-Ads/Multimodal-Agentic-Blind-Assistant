import pygame
import numpy as np

# Initialize the mixer - using 44.1kHz, 16-bit, and 2 channels (Stereo)
pygame.mixer.init(frequency=44100, size=-16, channels=2)

def play_beep(frequency=800, duration=0.1):
    """Generates and plays a sine wave beep compatible with stereo mixer."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    
    # Generate a smooth sine wave
    data = np.sin(2 * np.pi * frequency * t) * 0.3
    # Convert to 16-bit PCM
    audio_data = (data * 32767).astype(np.int16)
    
    # --- FIX: Convert Mono to Stereo ---
    # Reshape from (n,) to (n, 2) so pygame doesn't crash
    stereo_data = np.repeat(audio_data[:, np.newaxis], 2, axis=1)
    
    sound = pygame.sndarray.make_sound(stereo_data)
    sound.play()

def play_success_chime():
    """A quick double-beep to indicate 'I'm thinking'."""
    play_beep(600, 0.05)
    pygame.time.delay(50)
    play_beep(900, 0.05)

def play_error_chime():
    """A lower, longer beep for when no speech is detected."""
    play_beep(400, 0.2)

def play_stop_chime():
    """A descending double-beep that ensures it plays before exit."""
    play_beep(900, 0.07)
    pygame.time.delay(80) # Wait for first beep
    play_beep(600, 0.07)
    pygame.time.delay(150) # CRITICAL: Wait for second beep to finish