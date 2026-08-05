import time
import math
from collections import Counter, deque
from config import (
    STABILITY_THRESHOLD,
    PINCH_THRESHOLD,
    SWIPE_THRESHOLD,
    SWIPE_COOLDOWN,
    THUMBS_UP_HOLD,
    PINCH_HOLD,
    OPEN_PALM_HOLD,
    ACTION_COOLDOWN,
)

class GestureDetector:
    def __init__(self):
        """Initialise detection state, history queues and timers."""
        self.gesture_history = deque(maxlen=STABILITY_THRESHOLD)
        self.confirmed_gesture = "No Gesture"
        self.confirmed_fingers = 0
        # Timing & cooldown tracking
        self.current_raw = None
        self.start_time = None
        self.last_action_time = {}
        self.prev_palm_center = None
        self.last_swipe_time = 0

    # ------------------------ Utility helpers ------------------------
    def _calculate_distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

    def detect_open_palm(self, finger_states):
        return all(state == 1 for state in finger_states)

    def detect_thumbs_up(self, landmarks, finger_states):
        other_fingers_folded = all(state == 0 for state in finger_states[1:])
        # Allow a small tolerance when comparing Y coordinates of thumb landmarks
        tolerance = 0.02
        thumb_pointing_up = (landmarks[4][1] < landmarks[3][1] + tolerance) and (landmarks[3][1] < landmarks[2][1] + tolerance)
        return other_fingers_folded and thumb_pointing_up

    def detect_fist(self, finger_states):
        return all(state == 0 for state in finger_states)

    def detect_pinch(self, landmarks):
        return self._calculate_distance(landmarks[4], landmarks[8]) < PINCH_THRESHOLD

    def count_fingers(self, landmarks):
        if len(landmarks) < 21:
            return [0, 0, 0, 0, 0]
        finger_states = []
        # Thumb direction based on hand orientation
        if landmarks[5][0] > landmarks[17][0]:
            thumb_open = 1 if landmarks[4][0] < landmarks[3][0] else 0
        else:
            thumb_open = 1 if landmarks[4][0] > landmarks[3][0] else 0
        finger_states.append(thumb_open)
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        for tip, pip in zip(tips, pips):
            finger_states.append(1 if landmarks[tip][1] < landmarks[pip][1] else 0)
        return finger_states

    # ------------------------ Swipe detection ------------------------
    def _detect_swipe(self, palm_center):
        """Detect upward or downward swipe based on palm centre movement.
        Returns "Scroll Up", "Scroll Down" or None.
        """
        if self.prev_palm_center is None:
            self.prev_palm_center = palm_center
            return None
        delta_y = palm_center[1] - self.prev_palm_center[1]
        self.prev_palm_center = palm_center
        # Positive delta_y means moving downwards in image coordinates
        if delta_y < -SWIPE_THRESHOLD:
            return "Scroll Up"
        if delta_y > SWIPE_THRESHOLD:
            return "Scroll Down"
        return None

    # ------------------------ Cooldown handling ------------------------
    def _on_cooldown(self, action_name):
        """Return True if *action_name* is still on cooldown."""
        now = time.time()
        last = self.last_action_time.get(action_name, 0)
        return (now - last) < ACTION_COOLDOWN

    def _record_action(self, action_name):
        self.last_action_time[action_name] = time.time()

    # ------------------------ Core detection ------------------------
    def get_current_gesture(self, landmarks):
        """Determine the stabilized gesture, corresponding action, hold time and cooldown state.
        Returns a tuple: (gesture_name, action_name, hold_seconds, on_cooldown)
        """
        # No hand detected
        if not landmarks or len(landmarks) < 21:
            self.gesture_history.append(("No Hand", 0, None, 0.0, False))
            return "No Hand", None, 0.0, False

        finger_states = self.count_fingers(landmarks)
        finger_count = sum(finger_states)

        # Determine raw gesture name
        raw = "No Gesture"
        # Prioritize pinch detection before other gestures
        if self.detect_pinch(landmarks):
            raw = "Pinch"
        elif self.detect_thumbs_up(landmarks, finger_states):
            raw = "Thumbs Up"
        elif self.detect_open_palm(finger_states):
            raw = "Open Palm"
        elif self.detect_fist(finger_states):
            raw = "Fist"
        # Update timing for the raw gesture
        now = time.time()
        if raw != self.current_raw:
            self.current_raw = raw
            self.start_time = now
        hold_time = now - (self.start_time or now)

        # Determine action based on raw gesture and timing requirements
        action = None
        on_cooldown = False
        if raw == "Thumbs Up" and hold_time >= THUMBS_UP_HOLD:
            if not self._on_cooldown("Thumbs Up"):
                action = "Thumbs Up"
                self._record_action("Thumbs Up")
            else:
                on_cooldown = True
        elif raw == "Pinch" and hold_time >= PINCH_HOLD:
            if not self._on_cooldown("Pinch"):
                action = "Pinch"
                self._record_action("Pinch")
            else:
                on_cooldown = True
        elif raw == "Open Palm":
            # Swipe detection independent of open‑palm hold duration.
            palm_center = None
            if len(landmarks) >= 10:
                palm_center = landmarks[9][:2]
            if palm_center:
                swipe_action = self._detect_swipe(palm_center)
                if swipe_action:
                    # Enforce swipe cooldown separately
                    now = time.time()
                    if (now - self.last_swipe_time) >= SWIPE_COOLDOWN:
                        action = swipe_action
                        self.last_swipe_time = now
                        self._record_action(swipe_action)
                    else:
                        on_cooldown = True
        elif raw == "Fist":
            # Fist considered an immediate action (Cancel) – no hold required
            if not self._on_cooldown("Fist"):
                action = "Fist"
                self._record_action("Fist")
            else:
                on_cooldown = True

        # Append to history for stability smoothing of gesture name only
        self.gesture_history.append((raw, finger_count, action, hold_time, on_cooldown))
        if len(self.gesture_history) == STABILITY_THRESHOLD:
            # Majority vote for raw gesture
            raw_votes = Counter([g[0] for g in self.gesture_history])
            self.confirmed_gesture = raw_votes.most_common(1)[0][0]
            # Majority for action (ignoring None)
            actions = [g[2] for g in self.gesture_history if g[2] is not None]
            if actions:
                self.confirmed_action = Counter(actions).most_common(1)[0][0]
            else:
                self.confirmed_action = None
            self.confirmed_fingers = Counter([g[1] for g in self.gesture_history]).most_common(1)[0][0]
        else:
            self.confirmed_action = action
            self.confirmed_fingers = finger_count
            self.confirmed_gesture = raw

        return self.confirmed_gesture, self.confirmed_action, hold_time, on_cooldown
