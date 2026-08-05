import cv2
import mediapipe as mp
from config import DETECTION_CONFIDENCE, TRACKING_CONFIDENCE, MAX_HANDS

class HandTracker:
    def __init__(self):
        """Initialise MediaPipe Hands with custom tracking configurations."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_HANDS,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, frame, draw=True):
        """Detect hands in the frame and draw hand landmarks and connections."""
        # Convert BGR frame to RGB for MediaPipe processing
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_lms,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame

    def get_landmarks(self, frame):
        """Extract and return 21 hand landmark coordinates (normalized x, y, z)."""
        landmarks_list = []
        if self.results and self.results.multi_hand_landmarks:
            # We track the first hand detected (since max_hands = 1)
            hand_lms = self.results.multi_hand_landmarks[0]
            for lm in hand_lms.landmark:
                # Add normalized x, y, z coordinates
                landmarks_list.append((lm.x, lm.y, lm.z))
        return landmarks_list
