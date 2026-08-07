# VisionSwipe AI State Machine (Phase 6)
# Manages workflow transitions between NORMAL_MODE, SHARE_MODE, and CONFIRMING states.

import time
from enum import Enum, auto
from config import (
    SHARE_CONFIRM_HOLD,
    FINGER_HOLD,
    ACTION_COOLDOWN,
    THUMBS_UP_HOLD,
    PINCH_HOLD,
)
from instagram_controller import (
    scroll_up,
    scroll_down,
    like_post,
    open_share,
    select_friend,
    send_share,
    cancel_action,
)


class AppState(Enum):
    NORMAL_MODE = auto()
    SHARE_MODE = auto()
    CONFIRMING = auto()


class StateMachine:
    def __init__(self):
        self.state = AppState.NORMAL_MODE
        self.selected_friend = None
        self.last_action_time = {}
        self.status_message = "Normal Mode Active"

    def _is_on_cooldown(self, action_key: str, cooldown_duration: float = ACTION_COOLDOWN) -> bool:
        now = time.time()
        last = self.last_action_time.get(action_key, 0)
        return (now - last) < cooldown_duration

    def _record_action(self, action_key: str):
        self.last_action_time[action_key] = time.time()

    def process(self, gesture: str, action: str, finger_count: int, hold_time: float) -> tuple:
        """Process detected gesture and transition state machine.

        Args:
            gesture: Stabilized gesture string ('Open Palm', 'Thumbs Up', 'Pinch', 'Fist', '1 Finger', etc.)
            action: Evaluated action string from GestureDetector if any
            finger_count: Number of raised fingers (0 to 5)
            hold_time: Current hold duration in seconds for the active gesture

        Returns:
            Tuple of (state_name_str, status_message_str, executed_action_str)
        """
        handlers = {
            AppState.NORMAL_MODE: self._handle_normal_mode,
            AppState.SHARE_MODE: self._handle_share_mode,
            AppState.CONFIRMING: self._handle_confirming,
        }

        handler = handlers.get(self.state, self._handle_normal_mode)
        return handler(gesture, action, finger_count, hold_time)

    def _handle_normal_mode(self, gesture: str, action: str, finger_count: int, hold_time: float) -> tuple:
        executed_action = None

        if gesture == "Pinch" and (action == "Pinch" or hold_time >= PINCH_HOLD):
            if not self._is_on_cooldown("Pinch"):
                open_share()
                self._record_action("Pinch")
                self.state = AppState.SHARE_MODE
                self.selected_friend = None
                self.status_message = "Entered Share Mode"
                executed_action = "Open Share"

        elif gesture == "Thumbs Up" and (action == "Thumbs Up" or hold_time >= THUMBS_UP_HOLD):
            if not self._is_on_cooldown("Thumbs Up"):
                like_post()
                self._record_action("Thumbs Up")
                self.status_message = "Liked Current Reel"
                executed_action = "Like Post"

        elif gesture == "1 Finger" or (finger_count == 1 and gesture not in ["Thumbs Up", "Pinch", "Fist"]):
            if not self._is_on_cooldown("Scroll Down"):
                scroll_down()
                self._record_action("Scroll Down")
                self.status_message = "Previous Reel (1 Finger)"
                executed_action = "Previous Reel"

        elif gesture == "2 Fingers" or (finger_count == 2 and gesture not in ["Thumbs Up", "Pinch", "Fist"]):
            if not self._is_on_cooldown("Scroll Up"):
                scroll_up()
                self._record_action("Scroll Up")
                self.status_message = "Next Reel (2 Fingers)"
                executed_action = "Next Reel"

        elif gesture == "Fist":
            if not self._is_on_cooldown("Fist"):
                cancel_action()
                self._record_action("Fist")
                self.status_message = "Cancelled Action"
                executed_action = "Cancel"

        else:
            self.status_message = "Normal Mode - Ready"

        return self.state.name, self.status_message, executed_action

    def _handle_share_mode(self, gesture: str, action: str, finger_count: int, hold_time: float) -> tuple:
        executed_action = None

        if gesture == "Fist":
            if not self._is_on_cooldown("Fist"):
                cancel_action()
                self._record_action("Fist")
                self.state = AppState.NORMAL_MODE
                self.selected_friend = None
                self.status_message = "Share Cancelled"
                executed_action = "Cancel Share"

        elif gesture == "Open Palm":
            if self.selected_friend is not None:
                self.state = AppState.CONFIRMING
                return self._handle_confirming(gesture, action, finger_count, hold_time)
            else:
                self.status_message = "Select a friend first!"

        elif finger_count in [1, 2, 3, 4, 5]:
            friend_idx = finger_count
            key = f"Select Friend {friend_idx}"
            cooldown_key = "friend_selection"
            if not self._is_on_cooldown(cooldown_key, cooldown_duration=ACTION_COOLDOWN) and not self._is_on_cooldown(key, cooldown_duration=ACTION_COOLDOWN):
                select_friend(friend_idx)
                self._record_action(key)
                self._record_action(cooldown_key)
                self.selected_friend = friend_idx
                self.status_message = f"Selected Friend {friend_idx}"
                executed_action = f"Select Friend {friend_idx}"
            else:
                if self.selected_friend is not None:
                    self.status_message = f"Friend {self.selected_friend} Selected (Hold Open Palm to Send)"
                else:
                    self.status_message = "Share Mode - Show 1-5 Fingers"

        else:
            if self.selected_friend is not None:
                self.status_message = f"Friend {self.selected_friend} Selected (Hold Open Palm to Send)"
            else:
                self.status_message = "Share Mode - Show 1-5 Fingers"

        return self.state.name, self.status_message, executed_action

    def _handle_confirming(self, gesture: str, action: str, finger_count: int, hold_time: float) -> tuple:
        executed_action = None

        if gesture == "Open Palm":
            if hold_time >= SHARE_CONFIRM_HOLD:
                send_share()
                self._record_action("Send Share")
                friend = self.selected_friend
                self.state = AppState.NORMAL_MODE
                self.selected_friend = None
                self.status_message = f"Reel Shared to Friend {friend}!"
                executed_action = f"Sent Share to Friend {friend}"
            else:
                self.status_message = f"Confirming Send (Hold Open Palm {SHARE_CONFIRM_HOLD}s)..."
        elif gesture == "Fist":
            if not self._is_on_cooldown("Fist"):
                cancel_action()
                self._record_action("Fist")
                self.state = AppState.NORMAL_MODE
                self.selected_friend = None
                self.status_message = "Share Cancelled"
                executed_action = "Cancel Share"
        else:
            self.state = AppState.SHARE_MODE
            self.status_message = f"Friend {self.selected_friend} Selected (Hold Open Palm to Send)"

        return self.state.name, self.status_message, executed_action
