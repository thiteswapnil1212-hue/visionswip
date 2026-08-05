# VisionSwipe AI

VisionSwipe AI is a Python-based computer vision application designed to track hand gestures using MediaPipe and OpenCV, utilizing a robust State Machine architecture to automate Instagram web navigation and interactive Share workflows.

---

## Gesture Workflow (Phase 6 State Machine)

The application operates in two primary states managed by `state_machine.py`:

### 1. NORMAL MODE
| Gesture | Action | Description |
|---------|--------|-------------|
| 👍 **Thumbs Up** | Like | Clicks Instagram Like button (`like_post()`) |
| ☝️ **1 Finger** | Previous Reel | Scrolls down to previous Instagram reel |
| ✌️ **2 Fingers** | Next Reel | Scrolls up to next Instagram reel |
| 🤏 **Pinch** | Share Mode | Opens Instagram Share dialog & enters `SHARE_MODE` |
| ✊ **Fist** | Cancel | Presses `Esc` key to cancel dialogs |

---

### 2. SHARE MODE
When **Pinch** is detected in Normal Mode, the app enters **SHARE MODE** and displays an interactive webcam UI overlay.

| Gesture | Action | Description |
|---------|--------|-------------|
| ☝️ **1 Finger** | Select Friend 1 | Clicks Friend 1 position in Share dialog |
| ✌️ **2 Fingers** | Select Friend 2 | Clicks Friend 2 position in Share dialog |
| 🤟 **3 Fingers** | Select Friend 3 | Clicks Friend 3 position in Share dialog |
| 🖖 **4 Fingers** | Select Friend 4 | Clicks Friend 4 position in Share dialog |
| 🖐 **5 Fingers** | Select Friend 5 | Clicks Friend 5 position in Share dialog |
| ✋ **Open Palm (0.8s)** | Confirm Send | Confirms send, clicks Send button, exits to Normal Mode |
| ✊ **Fist** | Cancel | Cancels share dialog, closes overlay, returns to Normal Mode |

---

## Project Structure

```text
VisionSwipe_AI/
│
├── .venv/                      # Python virtual environment
├── main.py                     # Main loop displaying webcam feed, HUD & Share Mode overlay
├── hand_tracker.py             # HandTracker class utilizing MediaPipe
├── gesture_detector.py         # GestureDetector class detecting poses & finger counts
├── state_machine.py            # State Machine managing NORMAL_MODE, SHARE_MODE & CONFIRMING
├── instagram_controller.py     # PyAutoGUI mouse/keyboard interaction functions
├── config.py                   # Global parameters, timings & button screen coordinates
├── requirements.txt            # Project dependencies
├── test_env.py                 # Environment verification script
├── test_controller.py          # Manual test for controller functions
├── test_state_machine.py       # Automated unit test for State Machine transitions
├── test_gesture_pipeline.py    # Pipeline test for gesture detection
└── README.md                   # Project documentation
```

---

## Calibrating Screen Coordinates (`config.py`)

Instagram UI element locations vary depending on your monitor resolution and browser window position. Predefined coordinates are stored in `config.py`.

### How to Find Your Screen Coordinates:
1. Open Instagram in your web browser.
2. Open a Python terminal in your environment:
   ```python
   import pyautogui
   print(pyautogui.position())  # Move mouse over the target button and execute
   ```
3. Update `config.py` with the obtained pixel coordinates:

```python
# config.py
LIKE_BUTTON_POSITION = (1000, 500)   # Coordinates for Like button
SHARE_BUTTON_POSITION = (1200, 500)  # Coordinates for Share button
SEND_BUTTON_POSITION = (1000, 620)   # Coordinates for Send button in Share dialog

FRIEND_POSITIONS = {
    1: (1000, 300),  # Position for Friend 1 in list
    2: (1000, 360),  # Position for Friend 2 in list
    3: (1000, 420),  # Position for Friend 3 in list
    4: (1000, 480),  # Position for Friend 4 in list
    5: (1000, 540),  # Position for Friend 5 in list
}
```

### Safety Mode (`TEST_MODE`):
In `config.py`, set:
* `TEST_MODE = True`: Actions print to console without moving the mouse (safe testing).
* `TEST_MODE = False`: Executes real mouse and keyboard actions via PyAutoGUI.

---

## Setup & Running

### 1. Setup Virtual Environment
```bash
python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run State Machine Tests
```bash
python test_state_machine.py
```

### 4. Run Application
```bash
python main.py
```
* Press **`q`** in the video window to stop.
