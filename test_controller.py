# test_controller.py
# Comprehensive manual & automated test for Instagram controller functions.
# Run with `python test_controller.py`. Respects TEST_MODE setting from config.py.

import sys
from config import TEST_MODE
from instagram_controller import (
    scroll_up,
    scroll_down,
    like_post,
    open_share,
    select_friend,
    send_share,
    cancel_action,
)


def test_all_actions():
    print(f"\n==================================================")
    print(f"[TEST CONTROLLER] Testing all PyAutoGUI actions...")
    print(f"[TEST CONTROLLER] Current TEST_MODE = {TEST_MODE}")
    print(f"==================================================\n")

    actions = [
        ("Scroll Up (Next Reel)", scroll_up, []),
        ("Scroll Down (Previous Reel)", scroll_down, []),
        ("Like Post", like_post, []),
        ("Open Share Dialog", open_share, []),
        ("Select Friend 1", select_friend, [1]),
        ("Select Friend 2", select_friend, [2]),
        ("Select Friend 3", select_friend, [3]),
        ("Select Friend 4", select_friend, [4]),
        ("Select Friend 5", select_friend, [5]),
        ("Send Share", send_share, []),
        ("Cancel Action", cancel_action, []),
    ]

    passed = 0
    failed = 0

    for name, func, args in actions:
        print(f"--> Executing action: {name} ...")
        try:
            func(*args)
            print(f"    [SUCCESS] {name} executed without error.")
            passed += 1
        except Exception as e:
            print(f"    [ERROR] Failed to execute {name}: {e}", file=sys.stderr)
            failed += 1

    print(f"\n==================================================")
    print(f"[TEST CONTROLLER RESULTS] Passed: {passed}/{len(actions)}, Failed: {failed}/{len(actions)}")
    print(f"==================================================\n")

    assert failed == 0, f"{failed} controller action(s) failed."


def main():
    test_all_actions()


if __name__ == "__main__":
    main()
