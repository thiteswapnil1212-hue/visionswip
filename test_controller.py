'''test_controller.py
Simple manual test for Instagram controller functions.
Run with `python test_controller.py`. Ensure `TEST_MODE` is True for safety.
'''

from instagram_controller import (
    scroll_up,
    scroll_down,
    like_post,
    open_share,
    cancel_action,
)


def main():
    print("[TEST] Starting Instagram controller test (TEST_MODE expected)...")
    scroll_up()
    scroll_down()
    like_post()
    open_share()
    cancel_action()
    print("[TEST] Completed all controller actions.")


if __name__ == "__main__":
    main()
