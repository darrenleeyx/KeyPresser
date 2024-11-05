from threading import Event
from state.state import State
from state.state_changed_event import StateChangedEvent
from state.state_error_event import StateErrorEvent

class StateManager:
    def __init__(self, key_manager, log_manager):
        self.key_manager = key_manager
        self.log_manager = log_manager
        self.state = State.STOPPED
        self.state_changed_event = StateChangedEvent()
        self.state_error_event = StateErrorEvent()

    def update_state(self, new_state):
        self.state = new_state
        self.state_changed_event.set(new_state)

    def set_state_error(self, error):
        self.state_error_event.set(error)

    def toggle_state(self, key, interval_ms, min_interval_ms, should_alt_tab, should_random_delay):
        if self.state == State.STARTED:
            self.key_manager.stop_key_press()
            self.log_manager.log_info(f"Key press stopped.")
            self.update_state(State.STOPPED)
        elif self.state == State.STOPPED:
            if not self.key_manager.validate_key(key):
                self.set_state_error(f"Invalid key: '{key}'")
                return

            self.key_manager.start_key_press(key, interval_ms, min_interval_ms, should_alt_tab, should_random_delay)
            
            if self.key_manager.has_started:
                self.log_manager.log_info(f"Key press started for key '{key}' with interval {interval_ms} ms.")
                self.update_state(State.STARTED)
        else:
            self.log_manager.log_info(f"Unknown state: {self.state}")

