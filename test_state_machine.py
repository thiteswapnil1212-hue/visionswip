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


def test_share_mode_workflow_and_confirming():
    print("\n--- Testing Share Mode Workflow (NORMAL -> SHARE -> CONFIRMING -> NORMAL) ---")
    sm = StateMachine()

    # Step 1: Pinch -> Enter Share Mode
    state, msg, act = sm.process("Pinch", "Pinch", 2, 0.4)
    assert sm.state == AppState.SHARE_MODE, f"Expected SHARE_MODE, got {sm.state}"
    assert act == "Open Share", f"Expected 'Open Share', got '{act}'"
    print("[PASS] Pinch -> Entered SHARE_MODE")

    # Step 2: Select Friend 3 using 3 fingers
    time.sleep(1.1)
    state, msg, act = sm.process("3 Fingers", None, 3, 0.3)
    assert sm.selected_friend == 3, f"Expected friend 3, got {sm.selected_friend}"
    assert act == "Select Friend 3", f"Expected 'Select Friend 3', got '{act}'"
    print("[PASS] 3 Fingers -> Selected Friend 3")

    # Step 3: Short Open Palm hold (0.3s < SHARE_CONFIRM_HOLD) -> CONFIRMING state, no send action
    state, msg, act = sm.process("Open Palm", None, 5, 0.3)
    assert sm.state == AppState.CONFIRMING, f"Expected CONFIRMING state, got {sm.state}"
    assert act is None, f"Expected no action on short hold, got '{act}'"
    print("[PASS] Short Open Palm (0.3s) -> Entered CONFIRMING state without sending")

    # Step 4: Open Palm held continuously for >= SHARE_CONFIRM_HOLD (0.85s) -> Send share -> NORMAL_MODE
    state, msg, act = sm.process("Open Palm", None, 5, 0.85)
    assert sm.state == AppState.NORMAL_MODE, f"Expected NORMAL_MODE, got {sm.state}"
    assert act == "Sent Share to Friend 3", f"Expected 'Sent Share to Friend 3', got '{act}'"
    print("[PASS] Open Palm continuous hold (0.85s) -> Confirmed Send -> Returned to NORMAL_MODE")


def test_friend_selection_cooldown():
    print("\n--- Testing Friend Selection Cooldown ---")
    sm = StateMachine()

    # Enter SHARE_MODE
    sm.process("Pinch", "Pinch", 2, 0.4)
    assert sm.state == AppState.SHARE_MODE

    # Select Friend 4
    time.sleep(1.1)
    state, msg, act = sm.process("4 Fingers", None, 4, 0.3)
    assert sm.selected_friend == 4
    assert act == "Select Friend 4"
    print("[PASS] Selected Friend 4")

    # Immediate repeated 4 fingers detection (within cooldown) should be ignored
    state, msg, act = sm.process("4 Fingers", None, 4, 0.3)
    assert act is None, f"Expected repeated friend selection to be ignored, got '{act}'"
    assert sm.selected_friend == 4
    print("[PASS] Repeated 4 Fingers gesture ignored during cooldown")


def test_share_mode_cancel():
    print("\n--- Testing Share Mode Cancel Workflow ---")
    sm = StateMachine()

    # Step 1: Pinch -> Enter Share Mode
    sm.process("Pinch", "Pinch", 2, 0.4)
    assert sm.state == AppState.SHARE_MODE

    # Step 2: Select Friend 2
    time.sleep(1.1)
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
    print(f"Running Phase 6 State Machine unit tests (TEST_MODE={TEST_MODE})...")
    test_normal_mode_gestures()
    test_share_mode_workflow_and_confirming()
    test_friend_selection_cooldown()
    test_share_mode_cancel()
    print("\n[SUCCESS] All State Machine unit tests passed successfully!")


if __name__ == "__main__":
    main()
