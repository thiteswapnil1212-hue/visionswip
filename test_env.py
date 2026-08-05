import sys

def test_environment():
    print("=== Environment Verification ===")
    print(f"Python Version: {sys.version}")

    # Check OpenCV
    try:
        import cv2
        print(f"[OK] OpenCV is installed. Version: {cv2.__version__}")
    except ImportError as e:
        print(f"[FAIL] OpenCV import failed: {e}")

    # Check MediaPipe
    try:
        import mediapipe as mp
        print(f"[OK] MediaPipe is installed. Version: {mp.__version__}")
    except ImportError as e:
        print(f"[FAIL] MediaPipe import failed: {e}")

    # Check NumPy
    try:
        import numpy as np
        print(f"[OK] NumPy is installed. Version: {np.__version__}")
    except ImportError as e:
        print(f"[FAIL] NumPy import failed: {e}")

    # Check PyAutoGUI
    try:
        import pyautogui
        print("[OK] PyAutoGUI is installed.")
    except ImportError as e:
        print(f"[FAIL] PyAutoGUI import failed: {e}")

    # Check Camera Access
    print("\nChecking camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"[OK] Camera access successful. Captured frame shape: {frame.shape}")
            else:
                print("[WARNING] Camera opened but failed to read frame. (Could be in use or no camera connected)")
            cap.release()
        else:
            print("[WARNING] Could not open camera (ID 0). Make sure a camera is connected.")
    except Exception as e:
        print(f"[FAIL] Error checking camera: {e}")

if __name__ == "__main__":
    test_environment()
