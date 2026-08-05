# Instagram Interaction Controller (Phase 5B)
# This module now uses pyautogui to control Instagram actions.
# When TEST_MODE is True (default) actions are only printed for safety.

import time
import pyautogui
from config import (
    LIKE_BUTTON_POSITION,
    SHARE_BUTTON_POSITION,
    TEST_MODE,
)

# Small pause between pyautogui calls to avoid overwhelming the system
pyautogui.PAUSE = 0.1


def _safe_action(func, *args, **kwargs):
    """Execute a pyautogui action safely.

    If TEST_MODE is enabled the function is not executed; instead a message
    describing the intended action is printed. Any pyautogui exceptions are
    caught and reported so the main loop does not crash.
    """
    if TEST_MODE:
        print(f"[InstagramController][TEST_MODE] Would execute: {func.__name__}{args}")
        return
    try:
        func(*args, **kwargs)
    except Exception as e:
        print(f"[InstagramController][ERROR] {func.__name__} failed: {e}")


def scroll_up():
    """Scroll Instagram reels to the next reel.

    In Instagram the next reel is reached by scrolling *up* (positive scroll).
    """
    # A modest scroll amount works well for most screen resolutions.
    _safe_action(pyautogui.scroll, 500)
    time.sleep(0.2)  # brief delay after the action


def scroll_down():
    """Scroll Instagram reels to the previous reel.

    Scrolling *down* (negative scroll) moves to the previous reel.
    """
    _safe_action(pyautogui.scroll, -500)
    time.sleep(0.2)


def like_post():
    """Click the Instagram like button.

    The button coordinates are defined in ``config.LIKE_BUTTON_POSITION`` as a
    ``(x, y)`` tuple representing screen pixels.
    """
    x, y = LIKE_BUTTON_POSITION
    _safe_action(pyautogui.moveTo, x, y, duration=0.2)
    _safe_action(pyautogui.click)
    time.sleep(0.2)

def open_share():
    """Open the Instagram share dialog.

    Uses the screen coordinates from ``config.SHARE_BUTTON_POSITION``.
    """
    x, y = SHARE_BUTTON_POSITION
    _safe_action(pyautogui.moveTo, x, y, duration=0.2)
    _safe_action(pyautogui.click)
    time.sleep(0.2)

def cancel_action():
    """Cancel the current Instagram action (e.g., close dialogs).

    Sends an ``Esc`` key press.
    """
    _safe_action(pyautogui.press, "esc")
    time.sleep(0.2)

# Simple dispatcher that maps the high‑level action name returned by GestureDetector
# to the corresponding function defined above.

def dispatch_action(action_name: str):
    """Call the appropriate placeholder function based on *action_name*.

    Args:
        action_name: The action string produced by ``GestureDetector`` – one of
            "Scroll Up", "Scroll Down", "Thumbs Up", "Pinch", "Fist".
    """
    mapping = {
        "Scroll Up": scroll_up,
        "Scroll Down": scroll_down,
        "Thumbs Up": like_post,
        "Pinch": open_share,
        "Fist": cancel_action,
    }
    func = mapping.get(action_name)
    if func:
        func()
    # If the action is ``None`` or not recognised we simply do nothing.
