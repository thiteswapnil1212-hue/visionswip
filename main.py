import cv2
import time
import numpy as np
from config import CAMERA_ID, FRAME_WIDTH, FRAME_HEIGHT, SHARE_CONFIRM_HOLD
from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from state_machine import StateMachine, AppState


def draw_hud_and_overlay(frame, state_machine: StateMachine, gesture: str, action: str, hold_time: float, fps: float, fingers: int):
    # Mode Header Banner
    mode_name = state_machine.state.name
    if mode_name == "SHARE_MODE":
        banner_color = (0, 140, 255)  # Orange for Share Mode
    elif mode_name == "CONFIRMING":
        banner_color = (0, 255, 0)    # Green for Confirming
    else:
        banner_color = (255, 100, 0)  # Blue for Normal Mode

    # Draw Banner Top Bar
    cv2.rectangle(frame, (0, 0), (FRAME_WIDTH, 40), banner_color, -1)
    cv2.putText(frame, f"MODE: {mode_name} | {state_machine.status_message}", (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    # Left Stats Overlay
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Gesture: {gesture}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    cv2.putText(frame, f"Fingers: {fingers}", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)
    cv2.putText(frame, f"Hold: {hold_time:.2f}s", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # Share Mode Overlay Card
    if state_machine.state == AppState.SHARE_MODE:
        # Draw translucent overlay box on right half
        overlay = frame.copy()
        cv2.rectangle(overlay, (320, 50), (630, 320), (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        # Draw border
        cv2.rectangle(frame, (320, 50), (630, 320), (0, 140, 255), 2)

        # Overlay text content
        cv2.putText(frame, "--- SHARE MODE ---", (340, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
        cv2.putText(frame, "Show 1-5 fingers", (340, 115),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
        cv2.putText(frame, "to choose a friend.", (340, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)

        friend_text = f"Selected: Friend {state_machine.selected_friend}" if state_machine.selected_friend else "Selected: None"
        friend_color = (0, 255, 0) if state_machine.selected_friend else (200, 200, 200)
        cv2.putText(frame, friend_text, (340, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, friend_color, 2)

        cv2.putText(frame, "Open Palm = Confirm Send", (340, 220),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        cv2.putText(frame, "Fist = Cancel", (340, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Draw Hold Progress Bar if holding Open Palm for confirmation
        if gesture == "Open Palm" and state_machine.selected_friend:
            progress = min(1.0, hold_time / SHARE_CONFIRM_HOLD)
            bar_w = int(270 * progress)
            cv2.rectangle(frame, (340, 275), (610, 295), (100, 100, 100), 1)
            cv2.rectangle(frame, (340, 275), (340 + bar_w, 295), (0, 255, 0), -1)
            cv2.putText(frame, f"Confirming Send: {int(progress * 100)}%", (350, 290),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0) if progress > 0.5 else (255, 255, 255), 1)


def main():
    print("Starting VisionSwipe AI stream with State Machine...")
    print("Press 'q' in the window to exit.")

    # Initialize video capture
    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        print(f"Error: Could not open video source with ID {CAMERA_ID}.")
        return

    # Set frame dimensions
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    # Initialize components
    tracker = HandTracker()
    detector = GestureDetector()
    state_machine = StateMachine()

    prev_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                frame = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
                print("Warning: Failed to grab frame; using blank placeholder.")

            # Process hand tracking
            frame = tracker.find_hands(frame)
            landmarks = tracker.get_landmarks(frame)

            # Detect gesture
            gesture, action, hold_time, on_cooldown = detector.get_current_gesture(landmarks)
            fingers = detector.confirmed_fingers

            # Process State Machine logic
            mode_name, status_msg, executed_action = state_machine.process(
                gesture=gesture,
                action=action,
                finger_count=fingers,
                hold_time=hold_time,
            )

            if executed_action:
                print(f"[STATE MACHINE][{mode_name}] Executed Action: {executed_action}")

            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0.0
            prev_time = curr_time

            # Render HUD and Share Mode Overlay
            draw_hud_and_overlay(frame, state_machine, gesture, action, hold_time, fps, fingers)

            # Display window
            cv2.imshow("VisionSwipe AI - Hand & Gesture Feed", frame)

            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam stream stopped.")


if __name__ == "__main__":
    main()
