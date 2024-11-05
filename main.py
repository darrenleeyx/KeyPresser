import tkinter as tk
from keys.key_manager import KeyManager
from ui.ui_manager import UiManager
from logger.logger_manager import LoggerManager
from state.state_manager import StateManager
from threading import Thread
import fasteners
import os
import sys

lock_file_path = os.path.join(os.path.expanduser("~"), ".key_presser.lock")

lock = fasteners.InterProcessLock(lock_file_path)

if not lock.acquire(blocking=False):
    print("Another instance of this application is already running.")
    sys.exit(1)

try:
    if __name__ == "__main__":
        # Starting
        root = tk.Tk()
        key_manager = KeyManager()
        logger_manager = LoggerManager()
        state_manager = StateManager(key_manager, logger_manager)
        ui_manager = UiManager(root, state_manager)
        event_listener_thread = Thread(target=ui_manager.wait_for_state_changed_event, args=(state_manager.state_changed_event,))
        event_listener_thread.start()
        
        # Started
        root.mainloop()

        # Closing
        ui_manager.stop_event_listener_thread()
        if event_listener_thread.thread:
            event_listener_thread.join()

        key_manager.stop_key_press()
        key_manager.release_keys()
finally:
    lock.release()