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
SWIPE_THRESHOLD = 0.15            # Normalized vertical movement required for swipe
SWIPE_COOLDOWN = 1.0             # Seconds before another swipe can be triggered
THUMBS_UP_HOLD = 0.6             # Seconds thumb-up must be held
PINCH_HOLD = 0.4                 # Seconds pinch must be held
OPEN_PALM_HOLD = 1.2            # Seconds open palm must be held before confirming scroll
ACTION_COOLDOWN = 1.0           # Generic cooldown for any action

# Phase 5B – Instagram automation configuration
# Set TEST_MODE = True to run in safe mode (no mouse/keyboard actions). Set to False for real automation.
TEST_MODE = False  # Disable test mode for real Instagram interaction

# Phase 6 – Share Mode & State Machine configuration
SHARE_CONFIRM_HOLD = 0.8          # Hold duration for Open Palm in Share Mode to confirm send
FINGER_HOLD = 0.3                 # Hold duration for finger selection gestures

# Screen coordinates for Instagram UI elements (in pixels). Adjust these to match your screen resolution.
LIKE_BUTTON_POSITION = (1000, 500)   # Placeholder – move mouse here to click LIKE
SHARE_BUTTON_POSITION = (1200, 500)  # Placeholder – move mouse here to click SHARE
SEND_BUTTON_POSITION = (1000, 620)   # Placeholder – move mouse here to click SEND in share dialog

# Coordinates for selecting Friend 1 to 5 in Instagram share dialog
FRIEND_POSITIONS = {
    1: (1000, 300),
    2: (1000, 360),
    3: (1000, 420),
    4: (1000, 480),
    5: (1000, 540),
}

