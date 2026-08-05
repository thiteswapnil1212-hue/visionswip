import cv2
import time
from config import CAMERA_ID, FRAME_WIDTH, FRAME_HEIGHT
from hand_tracker import HandTracker
from gesture_detector import GestureDetector

def main():
    print("Starting VisionSwipe AI stream...")
    print("Press 'q' in the window to exit.")

    # Initialize video capture
    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        print(f"Error: Could not open video source with ID {CAMERA_ID}.")
        return

    # Set frame dimensions
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    # Initialize Hand Tracker and Gesture Detector
    tracker = HandTracker()
    detector = GestureDetector()

    prev_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to grab frame.")
                break

            # Process hand tracking and draw skeleton
            frame = tracker.find_hands(frame)
            landmarks = tracker.get_landmarks(frame)

            # Detect gesture and finger count
            gesture, fingers = detector.get_current_gesture(landmarks)

            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0.0
            prev_time = curr_time

            # Draw Information on Stream
            # Visual styles: Harmonious overlay with sleek background/contrast text
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, f"Gesture: {gesture}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            cv2.putText(frame, f"Fingers: {fingers}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # Display the stream
            cv2.imshow("VisionSwipe AI - Hand & Gesture Feed", frame)

            # Break loop on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Clean up resources
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam stream stopped.")

if __name__ == "__main__":
    main()
