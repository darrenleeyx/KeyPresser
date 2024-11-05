from threading import Event

class StateErrorEvent:
    def __init__(self):
        self.event = Event()
        self.error = None

    def set(self, error=None):
        self.error = error
        self.event.set()

    def wait(self, timeout=None):
        self.event.wait(timeout=timeout)
        return self.error

    def clear(self):
        self.event.clear()
        self.error = None