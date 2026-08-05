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

# Phase 4 timing & swipe parameters
SWIPE_THRESHOLD = 0.2            # Normalized vertical movement required for swipe
SWIPE_COOLDOWN = 1.0             # Seconds before another swipe can be triggered
THUMBS_UP_HOLD = 0.8             # Seconds thumb-up must be held
PINCH_HOLD = 0.5                 # Seconds pinch must be held
OPEN_PALM_HOLD = 1.5            # Seconds open palm must be held before confirming scroll
ACTION_COOLDOWN = 1.0           # Generic cooldown for any action

# Phase 5B – Instagram automation configuration
# Set TEST_MODE = True to run in safe mode (no mouse/keyboard actions). Set to False for real automation.
TEST_MODE = True

# Screen coordinates for Instagram UI elements (in pixels). Adjust these to match your screen resolution.
LIKE_BUTTON_POSITION = (1000, 500)   # Example placeholder – move mouse here to click LIKE
SHARE_BUTTON_POSITION = (1200, 500)  # Example placeholder – move mouse here to click SHARE
