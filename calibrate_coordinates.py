# calibrate_coordinates.py
# Coordinate Calibration Helper for VisionSwipe AI Instagram Automation
# Run with `python calibrate_coordinates.py`

import os
import re
import cv2
import pyautogui
import numpy as np
import config


def load_current_config():
    return {
        "LIKE_BUTTON_POSITION": getattr(config, "LIKE_BUTTON_POSITION", (1000, 500)),
        "SHARE_BUTTON_POSITION": getattr(config, "SHARE_BUTTON_POSITION", (1200, 500)),
        "SEND_BUTTON_POSITION": getattr(config, "SEND_BUTTON_POSITION", (1000, 620)),
        "FRIEND_POSITIONS": dict(getattr(config, "FRIEND_POSITIONS", {1: (1000, 300), 2: (1000, 360), 3: (1000, 420), 4: (1000, 480), 5: (1000, 540)})),
    }


def save_to_config_file(coords: dict, config_path: str = "config.py"):
    if not os.path.exists(config_path):
        print(f"[ERROR] {config_path} not found.")
        return False

    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update LIKE_BUTTON_POSITION
    content = re.sub(
        r"LIKE_BUTTON_POSITION\s*=\s*\([^)]+\)",
        f"LIKE_BUTTON_POSITION = {coords['LIKE_BUTTON_POSITION']}",
        content
    )

    # Update SHARE_BUTTON_POSITION
    content = re.sub(
        r"SHARE_BUTTON_POSITION\s*=\s*\([^)]+\)",
        f"SHARE_BUTTON_POSITION = {coords['SHARE_BUTTON_POSITION']}",
        content
    )

    # Update SEND_BUTTON_POSITION
    content = re.sub(
        r"SEND_BUTTON_POSITION\s*=\s*\([^)]+\)",
        f"SEND_BUTTON_POSITION = {coords['SEND_BUTTON_POSITION']}",
        content
    )

    # Format FRIEND_POSITIONS dictionary
    friend_dict_str = "FRIEND_POSITIONS = {\n"
    for k in sorted(coords["FRIEND_POSITIONS"].keys()):
        friend_dict_str += f"    {k}: {coords['FRIEND_POSITIONS'][k]},\n"
    friend_dict_str += "}"

    content = re.sub(
        r"FRIEND_POSITIONS\s*=\s*\{[^}]*\}",
        friend_dict_str,
        content
    )

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[SUCCESS] Updated {config_path} with calibrated coordinates!")
    return True


def main():
    print("==========================================================")
    print(" VisionSwipe AI - Coordinate Calibration Tool")
    print("==========================================================")
    print("Move your mouse cursor over the Instagram UI elements")
    print("and press the key corresponding to that element:\n")
    print("  L     - Save Like Button Position")
    print("  S     - Save Share Button Position")
    print("  1-5   - Save Friend 1-5 Position")
    print("  E     - Save Send Button Position")
    print("  W     - Write/Save Calibrated Coordinates to config.py")
    print("  Q     - Quit Calibration Tool")
    print("==========================================================\n")

    coords = load_current_config()
    status_msg = "Calibrator Ready. Move mouse and press key."

    window_name = "VisionSwipe AI - Coordinate Calibrator"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    while True:
        # Get live mouse position from PyAutoGUI
        x, y = pyautogui.position()

        # Create blank canvas for HUD (width 640, height 520)
        img = np.zeros((540, 680, 3), dtype=np.uint8)

        # Header banner
        cv2.rectangle(img, (0, 0), (680, 45), (255, 120, 0), -1)
        cv2.putText(img, "VisionSwipe AI - Coordinate Calibrator", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Live Mouse Pos Box
        cv2.rectangle(img, (20, 60), (660, 110), (40, 40, 40), -1)
        cv2.rectangle(img, (20, 60), (660, 110), (0, 255, 255), 2)
        cv2.putText(img, f"Current Mouse Position: X={x}, Y={y}", (35, 93),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)

        # Saved Coordinates Table
        y_offset = 140
        cv2.putText(img, "Target Coordinates:", (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        y_offset += 25
        cv2.putText(img, f"[L] Like Button: {coords['LIKE_BUTTON_POSITION']}", (40, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)

        y_offset += 25
        cv2.putText(img, f"[S] Share Button: {coords['SHARE_BUTTON_POSITION']}", (40, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)

        y_offset += 25
        cv2.putText(img, f"[E] Send Button:  {coords['SEND_BUTTON_POSITION']}", (40, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 1)

        for idx in range(1, 6):
            y_offset += 25
            pos = coords["FRIEND_POSITIONS"].get(idx, (0, 0))
            cv2.putText(img, f"[{idx}] Friend {idx} Pos: {pos}", (40, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 200, 0), 1)

        # Controls & Status bar
        cv2.rectangle(img, (0, 480), (680, 540), (20, 20, 20), -1)
        cv2.putText(img, "[W] Save to config.py  |  [Q] Quit", (20, 505), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 200, 255), 1)
        cv2.putText(img, f"Status: {status_msg}", (20, 528), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imshow(window_name, img)

        key = cv2.waitKey(50) & 0xFF

        if key in [ord('q'), ord('Q'), 27]:  # ESC or Q
            print("[CALIBRATION] Exiting calibration tool.")
            break
        elif key in [ord('l'), ord('L')]:
            coords["LIKE_BUTTON_POSITION"] = (x, y)
            status_msg = f"Set LIKE_BUTTON_POSITION to ({x}, {y})"
            print(f"[CALIBRATE] {status_msg}")
        elif key in [ord('s'), ord('S')]:
            coords["SHARE_BUTTON_POSITION"] = (x, y)
            status_msg = f"Set SHARE_BUTTON_POSITION to ({x}, {y})"
            print(f"[CALIBRATE] {status_msg}")
        elif key in [ord('e'), ord('E'), 13]:  # E or Enter
            coords["SEND_BUTTON_POSITION"] = (x, y)
            status_msg = f"Set SEND_BUTTON_POSITION to ({x}, {y})"
            print(f"[CALIBRATE] {status_msg}")
        elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
            friend_num = int(chr(key))
            coords["FRIEND_POSITIONS"][friend_num] = (x, y)
            status_msg = f"Set Friend {friend_num} Position to ({x}, {y})"
            print(f"[CALIBRATE] {status_msg}")
        elif key in [ord('w'), ord('W')]:
            if save_to_config_file(coords):
                status_msg = "Successfully saved all coordinates to config.py!"

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
