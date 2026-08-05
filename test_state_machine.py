# Unit test for Phase 6 State Machine & Workflow

import time
from state_machine import StateMachine, AppState
from config import TEST_MODE


def test_normal_mode_gestures():
    print("\n--- Testing Normal Mode Gestures ---")
    sm = StateMachine()

    # 1. Thumbs Up -> Like Post
    state, msg, act = sm.process("Thumbs Up", "Thumbs Up", 1, 0.6)
    assert act == "Like Post", f"Expected 'Like Post', got '{act}'"
    print("[PASS] Thumbs Up -> Like Post")

    # 2. 1 Finger -> Previous Reel
    time.sleep(1.1)  # cooldown clearance
    state, msg, act = sm.process("1 Finger", None, 1, 0.3)
    assert act == "Previous Reel", f"Expected 'Previous Reel', got '{act}'"
    print("[PASS] 1 Finger -> Previous Reel")

    # 3. 2 Fingers -> Next Reel
    time.sleep(1.1)
    state, msg, act = sm.process("2 Fingers", None, 2, 0.3)
    assert act == "Next Reel", f"Expected 'Next Reel', got '{act}'"
    print("[PASS] 2 Fingers -> Next Reel")

    # 4. Fist -> Cancel
    time.sleep(1.1)
    state, msg, act = sm.process("Fist", "Fist", 0, 0.1)
    assert act == "Cancel", f"Expected 'Cancel', got '{act}'"
    print("[PASS] Fist -> Cancel")


def test_share_mode_workflow():
    print("\n--- Testing Share Mode Workflow ---")
    sm = StateMachine()

    # Step 1: Pinch -> Enter Share Mode
    state, msg, act = sm.process("Pinch", "Pinch", 2, 0.4)
    assert sm.state == AppState.SHARE_MODE, f"Expected SHARE_MODE, got {sm.state}"
    assert act == "Open Share", f"Expected 'Open Share', got '{act}'"
    print("[PASS] Pinch -> Entered SHARE_MODE")

    # Step 2: Select Friend 3 using 3 fingers
    time.sleep(0.6)
    state, msg, act = sm.process("3 Fingers", None, 3, 0.3)
    assert sm.selected_friend == 3, f"Expected friend 3, got {sm.selected_friend}"
    assert act == "Select Friend 3", f"Expected 'Select Friend 3', got '{act}'"
    print("[PASS] 3 Fingers -> Selected Friend 3")

    # Step 3: Open Palm held for 0.8s -> Confirm Send -> Returns to NORMAL_MODE
    time.sleep(1.1)
    state, msg, act = sm.process("Open Palm", None, 5, 0.85)
    assert sm.state == AppState.NORMAL_MODE, f"Expected NORMAL_MODE, got {sm.state}"
    assert "Sent Share to Friend 3" in act, f"Expected 'Sent Share to Friend 3', got '{act}'"
    print("[PASS] Open Palm (0.85s) -> Confirmed Send -> Returned to NORMAL_MODE")


def test_share_mode_cancel():
    print("\n--- Testing Share Mode Cancel Workflow ---")
    sm = StateMachine()

    # Step 1: Pinch -> Enter Share Mode
    sm.process("Pinch", "Pinch", 2, 0.4)
    assert sm.state == AppState.SHARE_MODE

    # Step 2: Select Friend 2
    time.sleep(0.6)
    sm.process("2 Fingers", None, 2, 0.3)
    assert sm.selected_friend == 2

    # Step 3: Fist -> Cancel -> Returns to NORMAL_MODE without sending
    time.sleep(1.1)
    state, msg, act = sm.process("Fist", "Fist", 0, 0.1)
    assert sm.state == AppState.NORMAL_MODE, f"Expected NORMAL_MODE, got {sm.state}"
    assert sm.selected_friend is None, f"Expected selected_friend None, got {sm.selected_friend}"
    assert act == "Cancel Share", f"Expected 'Cancel Share', got '{act}'"
    print("[PASS] Fist -> Cancel Share -> Returned to NORMAL_MODE")


def main():
    print(f"Running Phase 6 State Machine tests (TEST_MODE={TEST_MODE})...")
    test_normal_mode_gestures()
    test_share_mode_workflow()
    test_share_mode_cancel()
    print("\n[SUCCESS] All State Machine unit tests passed successfully!")


if __name__ == "__main__":
    main()
