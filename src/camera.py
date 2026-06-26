import cv2
import os

# Persistent capture object to avoid initialization lag
_cap = None

def capture_image(filename="data/capture.jpg"):
    global _cap
    if not os.path.exists('data'): 
        os.makedirs('data')
    
    # Initialize only if not already open
    if _cap is None or not _cap.isOpened():
        _cap = cv2.VideoCapture(0)
    
    # Grab and retrieve the latest frame
    # We grab once to flush any old frame in the buffer
    _cap.grab()
    ret, frame = _cap.read()
    
    if ret:
        # Resize for faster API upload and processing
        small_frame = cv2.resize(frame, (640, 480))
        cv2.imwrite(filename, small_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        return filename
    return None

def release_camera():
    global _cap
    if _cap:
        _cap.release()