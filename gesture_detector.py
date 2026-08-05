import math
from collections import Counter
from config import STABILITY_THRESHOLD, PINCH_THRESHOLD

class GestureDetector:
    def __init__(self):
        """Initialise the gesture detector with a history queue for stability."""
        self.gesture_history = []
        self.confirmed_gesture = "No Gesture"
        self.confirmed_fingers = 0

    def _calculate_distance(self, p1, p2):
        """Calculate Euclidean distance between two 3D landmarks."""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

    def detect_open_palm(self, finger_states):
        """Check if all five fingers are extended."""
        return all(state == 1 for state in finger_states)

    def detect_thumbs_up(self, landmarks, finger_states):
        """Check if thumb is pointing up and other fingers are folded."""
        # Other fingers must be folded
        other_fingers_folded = all(state == 0 for state in finger_states[1:])
        # Thumb tip must be higher (lower y) than thumb IP and MCP
        thumb_pointing_up = landmarks[4][1] < landmarks[3][1] < landmarks[2][1]
        return other_fingers_folded and thumb_pointing_up

    def detect_fist(self, finger_states):
        """Check if all fingers are folded."""
        return all(state == 0 for state in finger_states)

    def detect_pinch(self, landmarks):
        """Check if the distance between thumb tip and index tip is below threshold."""
        dist = self._calculate_distance(landmarks[4], landmarks[8])
        return dist < PINCH_THRESHOLD

    def count_fingers(self, landmarks):
        """Determine extension state (1 = extended, 0 = folded) of each finger."""
        if len(landmarks) < 21:
            return [0, 0, 0, 0, 0]

        finger_states = []

        # Thumb extension check based on hand orientation
        # Check if thumb tip (4) is to the outer side of the hand compared to joint 3/2.
        # Compare index MCP (5) and pinky MCP (17) to determine orientation
        if landmarks[5][0] > landmarks[17][0]:
            # Hand facing camera or right hand
            thumb_open = 1 if landmarks[4][0] < landmarks[3][0] else 0
        else:
            # Hand back facing camera or left hand
            thumb_open = 1 if landmarks[4][0] > landmarks[3][0] else 0
        
        finger_states.append(thumb_open)

        # 4 Fingers (Index, Middle, Ring, Pinky)
        # Finger is extended if tip y-coordinate is higher (lower y) than PIP joint y-coordinate
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        for tip, pip in zip(tips, pips):
            finger_states.append(1 if landmarks[tip][1] < landmarks[pip][1] else 0)

        return finger_states

    def get_current_gesture(self, landmarks):
        """Calculate, smooth, and return the current gesture and finger count."""
        if not landmarks or len(landmarks) < 21:
            self.gesture_history.append(("No Hand", 0))
            if len(self.gesture_history) > STABILITY_THRESHOLD:
                self.gesture_history.pop(0)
            return "No Hand", 0

        finger_states = self.count_fingers(landmarks)
        finger_count = sum(finger_states)

        # Determine gesture
        raw_gesture = "No Gesture"
        if self.detect_thumbs_up(landmarks, finger_states):
            raw_gesture = "Thumbs Up"
        elif self.detect_open_palm(finger_states):
            raw_gesture = "Open Palm"
        elif self.detect_fist(finger_states):
            raw_gesture = "Fist"
        elif self.detect_pinch(landmarks):
            raw_gesture = "Pinch"

        # Stability logic: append raw detection and average/majority vote
        self.gesture_history.append((raw_gesture, finger_count))
        if len(self.gesture_history) > STABILITY_THRESHOLD:
            self.gesture_history.pop(0)

        # Majority vote for gesture name
        gestures_in_history = [g[0] for g in self.gesture_history]
        gesture_counts = Counter(gestures_in_history)
        self.confirmed_gesture = gesture_counts.most_common(1)[0][0]

        # Majority vote for finger count
        fingers_in_history = [g[1] for g in self.gesture_history]
        finger_counts = Counter(fingers_in_history)
        self.confirmed_fingers = finger_counts.most_common(1)[0][0]

        return self.confirmed_gesture, self.confirmed_fingers
