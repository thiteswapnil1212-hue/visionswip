import cv2
import mediapipe as mp
from config import DETECTION_CONFIDENCE, TRACKING_CONFIDENCE, MAX_HANDS

class HandTracker:
    def __init__(self):
        """Initialise MediaPipe Hands with custom tracking configurations."""
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_HANDS,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, frame, draw=True):
        """Detect hands in the frame and optionally draw landmarks."""
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks and draw:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_lms,
                    mp.solutions.hands.HAND_CONNECTIONS,
                )
        return frame

    def get_landmarks(self, frame):
        """Return list of 21 normalized (x, y, z) landmark tuples for the first hand."""
        landmarks_list = []
        if self.results and self.results.multi_hand_landmarks:
            hand_lms = self.results.multi_hand_landmarks[0]
            for lm in hand_lms.landmark:
                landmarks_list.append((lm.x, lm.y, lm.z))
        return landmarks_list

    def get_palm_center(self):
        """Return the normalized (x, y) coordinate of the palm centre (landmark 9).
        Returns ``None`` if no hand is detected.
        """
        if self.results and self.results.multi_hand_landmarks:
            lm = self.results.multi_hand_landmarks[0].landmark[9]
            return (lm.x, lm.y)
        return None
