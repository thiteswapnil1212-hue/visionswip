# Test script for final gesture pipeline verification (Phase 5B)
# Run with TEST_MODE=True for safe execution.

import time
import copy
from gesture_detector import GestureDetector
from config import (
    SWIPE_THRESHOLD,
    SWIPE_COOLDOWN,
    THUMBS_UP_HOLD,
    PINCH_HOLD,
    OPEN_PALM_HOLD,
    ACTION_COOLDOWN,
    STABILITY_THRESHOLD,
    TEST_MODE,
)

# Helper to generate dummy landmarks based on finger openness flags.
# flags: list of 5 bools for thumb, index, middle, ring, pinky (True=extended)
def generate_landmarks(flags):
    # Create 21 landmarks with (x, y, z) normalized values.
    # We'll keep x simple and use y to encode finger state.
    # For thumb orientation we assume hand facing palm-up (landmarks[5] > landmarks[17]).
    landmarks = [(0.5, 0.5, 0.0) for _ in range(21)]
    # Thumb: landmarks 4 (tip) and 3 (ip)
    if flags[0]:
        landmarks[4] = (0.7, 0.4, 0.0)  # tip right of ip => open for this orientation
    else:
        landmarks[4] = (0.3, 0.6, 0.0)  # tip left of ip => closed
    landmarks[3] = (0.5, 0.5, 0.0)
    # Other fingers: tip indices 8,12,16,20 ; pip indices 6,10,14,18
    tip_indices = [8, 12, 16, 20]
    pip_indices = [6, 10, 14, 18]
    for i, open_f in enumerate(flags[1:]):
        tip = tip_indices[i]
        pip = pip_indices[i]
        if open_f:
            # tip higher (smaller y) than pip
            landmarks[tip] = (0.5, 0.3, 0.0)
            landmarks[pip] = (0.5, 0.5, 0.0)
        else:
            # tip lower (larger y) than pip
            landmarks[tip] = (0.5, 0.7, 0.0)
            landmarks[pip] = (0.5, 0.5, 0.0)
    # Palm centre (landmark 9) – set to middle of hand for swipe testing later.
    landmarks[9] = (0.5, 0.5, 0.0)
    # Additional landmarks can stay default.
    return landmarks

# Simulate a sequence of frames for a specific gesture.

def simulate_gesture(name, frames, hold_seconds, expected_action):
    detector = GestureDetector()
    start = time.time()
    action_triggered = None
    print(f"\n--- Simulating {name} ---")
    for i, lm in enumerate(frames):
        gesture, action, hold, cooldown = detector.get_current_gesture(lm)
        print(f"Frame {i+1}: gesture={gesture}, action={action}, hold={hold:.2f}s, cooldown={cooldown}")
        if action:
            action_triggered = action
        # wait a bit to emulate real time (0.2s per frame)
        time.sleep(0.2)
    elapsed = time.time() - start
    print(f"Total simulated time: {elapsed:.2f}s")
    if action_triggered == expected_action:
        print(f"[PASS] Expected action '{expected_action}' detected.")
    else:
        print(f"[FAIL] Expected '{expected_action}', got '{action_triggered}'.")

# 1. Open Palm swipe up
open_palm_landmarks = generate_landmarks([True, True, True, True, True])
# Create frames: hold open palm for required time, then move palm up.
frames_up = []
# hold period (STABILITY_THRESHOLD frames ~ 5) with same palm centre
for _ in range(STABILITY_THRESHOLD):
    frames_up.append(open_palm_landmarks)
# swipe up: move palm centre y downwards (negative delta)
up_moved = list(open_palm_landmarks)
up_moved[9] = (0.5, 0.2, 0.0)  # significant upward movement
frames_up.append(up_moved)
# Add a few more frames to let cooldown settle
for _ in range(2):
    frames_up.append(open_palm_landmarks)

simulate_gesture("Open Palm Swipe Up", frames_up, OPEN_PALM_HOLD + 0.5, "Scroll Up")

# 2. Open Palm swipe down
frames_down = []
for _ in range(STABILITY_THRESHOLD):
    frames_down.append(open_palm_landmarks)
# move palm centre downwards
down_moved = list(open_palm_landmarks)
down_moved[9] = (0.5, 0.8, 0.0)
frames_down.append(down_moved)
for _ in range(2):
    frames_down.append(open_palm_landmarks)

simulate_gesture("Open Palm Swipe Down", frames_down, OPEN_PALM_HOLD + 0.5, "Scroll Down")

# 3. Thumbs Up (hold required)
thumbs_up_landmarks = generate_landmarks([True, False, False, False, False])
# Simulate hold frames
frames_thumb = []
for _ in range(int(THUMBS_UP_HOLD / 0.2) + 2):  # enough frames to exceed hold time
    frames_thumb.append(thumbs_up_landmarks)
simulate_gesture("Thumbs Up", frames_thumb, THUMBS_UP_HOLD, "Thumbs Up")

# 4. Pinch (hold required)
# For pinch we need thumb tip close to index tip.
def generate_pinch_landmarks():
    lm = generate_landmarks([True, True, False, False, False])
    # Bring thumb tip (4) close to index tip (8)
    lm[4] = (0.5, 0.5, 0.0)
    lm[8] = (0.5, 0.5, 0.0)
    return lm
pinch_landmarks = generate_pinch_landmarks()
frames_pinch = []
for _ in range(int(PINCH_HOLD / 0.2) + 2):
    frames_pinch.append(pinch_landmarks)
simulate_gesture("Pinch", frames_pinch, PINCH_HOLD, "Pinch")

# 5. Fist (immediate)
fist_landmarks = generate_landmarks([False, False, False, False, False])
frames_fist = [fist_landmarks]
simulate_gesture("Fist", frames_fist, 0, "Fist")

print("\nTesting complete. Review the PASS/FAIL messages above.")
