import pygame
import numpy as np

# Instantiate standard stereo mixer configurations with custom frequency profiles
pygame.mixer.init(frequency=44100, size=-16, channels=2)

def play_beep(frequency=800, duration=0.1):
    """
    Computes a mathematical 16-bit sine wave vector, maps mono configurations 
    into a structured dual-channel matrix, and triggers immediate audio execution.
    """
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, False)
    
    data = np.sin(2 * np.pi * frequency * t) * 0.3
    audio_data = (data * 32767).astype(np.int16)
    
    # Linearly projecting 1D mono vectors into a valid 2D multi-channel stereo space
    stereo_data = np.repeat(audio_data[:, np.newaxis], 2, axis=1)
    
    sound = pygame.sndarray.make_sound(stereo_data)
    sound.play()

def play_success_chime():
    """Dispatches a dynamic dual ascending tone validating data capture."""
    play_beep(600, 0.05)
    pygame.time.delay(50)
    play_beep(900, 0.05)

def play_error_chime():
    """Dispatches a continuous low-frequency flat tone indicating a system fault."""
    play_beep(400, 0.2)

def play_stop_chime():
    """Executes a clean descending acoustic tone sequence prior to system teardown."""
    play_beep(900, 0.07)
    pygame.time.delay(80) 
    play_beep(600, 0.07)
    pygame.time.delay(150)