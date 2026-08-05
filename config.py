# Configuration settings for VisionSwipe AI
import os

# Webcam settings
CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# MediaPipe Hand Tracking parameters
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.7
MAX_HANDS = 1

# GestureDetector stability parameters
STABILITY_THRESHOLD = 5
PINCH_THRESHOLD = 0.04  # Normalised distance threshold between thumb tip and index tip
