import cv2
import time
import numpy as np
from config import CAMERA_ID, FRAME_WIDTH, FRAME_HEIGHT, SHARE_CONFIRM_HOLD
from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from state_machine import StateMachine, AppState


def draw_hud_and_overlay(frame, state_machine: StateMachine, gesture: str, action: str, executed_action: str, hold_time: float, fps: float, fingers: int, on_cooldown: bool):
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
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Left Stats Overlay Card
    overlay_bg = frame.copy()
    cv2.rectangle(overlay_bg, (5, 45), (310, 245), (20, 20, 20), -1)
    cv2.addWeighted(overlay_bg, 0.65, frame, 0.35, 0, frame)

    cooldown_str = "ACTIVE" if on_cooldown else "READY"
    cooldown_color = (0, 0, 255) if on_cooldown else (0, 255, 0)
    act_display = executed_action if executed_action else (action if action else "None")
    friend_display = f"Friend {state_machine.selected_friend}" if state_machine.selected_friend else "None"

    cv2.putText(frame, f"Current Mode: {mode_name}", (12, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"Current Gesture: {gesture}", (12, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(frame, f"Current Action: {act_display}", (12, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    cv2.putText(frame, f"Selected Friend: {friend_display}", (12, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 0), 1)
    cv2.putText(frame, f"Hold Timer: {hold_time:.2f}s", (12, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 150), 1)
    cv2.putText(frame, f"Cooldown Status: {cooldown_str}", (12, 195), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cooldown_color, 1)
    cv2.putText(frame, f"FPS: {int(fps)} | Fingers: {fingers}", (12, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    # Share Mode Overlay Card
    if state_machine.state in [AppState.SHARE_MODE, AppState.CONFIRMING]:
        overlay = frame.copy()
        cv2.rectangle(overlay, (320, 45), (630, 245), (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        card_color = (0, 255, 0) if state_machine.state == AppState.CONFIRMING else (0, 140, 255)
        cv2.rectangle(frame, (320, 45), (630, 245), card_color, 2)

        cv2.putText(frame, "SHARE MODE ACTIVE", (340, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
        cv2.putText(frame, "Show 1-5 fingers to choose friend", (330, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1)
        cv2.putText(frame, f"Selected Friend: {friend_display}", (330, 135),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0) if state_machine.selected_friend else (180, 180, 180), 2)

        cv2.putText(frame, "Open Palm = Confirm", (330, 165),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        cv2.putText(frame, "Fist = Cancel", (330, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Hold progress bar
        if gesture == "Open Palm" and state_machine.selected_friend:
            progress = min(1.0, hold_time / SHARE_CONFIRM_HOLD)
            bar_w = int(270 * progress)
            cv2.rectangle(frame, (330, 215), (610, 235), (80, 80, 80), 1)
            cv2.rectangle(frame, (330, 215), (330 + bar_w, 235), (0, 255, 0), -1)
            cv2.putText(frame, f"Confirming Send: {int(progress * 100)}%", (340, 230),
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
            draw_hud_and_overlay(frame, state_machine, gesture, action, executed_action, hold_time, fps, fingers, on_cooldown)

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
