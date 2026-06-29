import cv2
import os

# Singleton reference pattern to hold the camera context and prevent initialization latencies
_cap = None

def capture_image(filename="data/capture.jpg"):
    """
    Flushes the underlying frame buffer cache, grabs the most recent high-frequency image array,
    resizes it for rapid network transport, and writes it to disk.
    """
    global _cap
    if not os.path.exists('data'): 
        os.makedirs('data')
    
    if _cap is None or not _cap.isOpened():
        _cap = cv2.VideoCapture(0)
    
    # Dual-pass invocation to ensure frame cache optimization and prevent visual drift
    _cap.grab()
    ret, frame = _cap.read()
    
    if ret:
        small_frame = cv2.resize(frame, (640, 480))
        cv2.imwrite(filename, small_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        return filename
    return None

def release_camera():
    """Gracefully releases video capture resources to unblock system hardware hooks."""
    global _cap
    if _cap:
        _cap.release()