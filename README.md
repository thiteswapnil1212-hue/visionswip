# VisionSwipe AI

VisionSwipe AI is a Python-based computer vision application designed to track hand gestures using MediaPipe and OpenCV, preparing a foundation for automation (such as Instagram scrolling controls).

## Project Structure

```text
VisionSwipe_AI/
│
├── .venv/                      # Python virtual environment (ignored by Git)
├── main.py                     # Main webcam loop displaying landmarks and gestures
├── hand_tracker.py             # HandTracker class utilizing MediaPipe
├── gesture_detector.py         # GestureDetector class detecting specific shapes/poses
├── instagram_controller.py     # Controls for Instagram interactions (placeholder)
├── config.py                   # Global tracking and layout parameters
├── requirements.txt            # Project dependencies
├── test_env.py                 # Verification test for environment capability
├── .gitignore                  # Standard git exclusions
└── README.md                   # Installation and usage instructions
```

## Step-by-Step Setup Instructions

### 1. Create a Python Virtual Environment

Create a clean, isolated environment using Python's built-in `venv` module. Run the following command in your terminal:

```bash
python -m venv .venv
```

### 2. Activate the Virtual Environment

Activate the environment based on your operating system:

#### Windows (PowerShell)
```powershell
.\.venv\Scripts\Activate.ps1
```

#### Windows (CMD)
```cmd
.\.venv\Scripts\activate.bat
```

#### Linux / macOS (Bash/Zsh)
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required core libraries (OpenCV, MediaPipe, NumPy, PyAutoGUI) and development modules:

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

Run the automated validation script to ensure all modules are successfully imported and your camera is reachable:

```bash
python test_env.py
```

Expected Output:
```text
=== Environment Verification ===
Python Version: 3.x.x
[OK] OpenCV is installed. Version: 5.x.x
[OK] MediaPipe is installed. Version: 1.x.x
[OK] NumPy is installed. Version: 2.x.x
[OK] PyAutoGUI is installed.

Checking camera access...
[OK] Camera access successful. Captured frame shape: (480, 640, 3)
```

### 5. Run the Project

Launch the main live stream application:

```bash
python main.py
```

*   **Move your hand** in front of the camera to see the real-time landmark tracking.
*   **Try Gestures:** Fist, Open Palm, Thumbs Up, Pinch, or show any number of fingers (0-5).
*   **Press `q`** inside the webcam window to safely exit.
