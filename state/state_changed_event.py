from threading import Event
from state.state import State

class StateChangedEvent:
    def __init__(self):
        self.event = Event()
        self.state = None

    def set(self, state=State.UNKNOWN):
        self.state = state
        self.event.set()

    def wait(self, timeout=None):
        self.event.wait(timeout=timeout)
        return self.state

    def clear(self):
        self.event.clear()
        self.state = None