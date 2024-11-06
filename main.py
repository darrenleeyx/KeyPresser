import tkinter as tk
from tkinter import messagebox
from __settings__.settings_manager import SettingsManager
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
    messagebox.showerror("Error", "Another instance of this application is already running.")
    sys.exit(1)

try:
    root = tk.Tk()
    logger_manager = LoggerManager()

    if __name__ == "__main__":
        try:
            settings_manager = SettingsManager()
            key_manager = KeyManager(logger_manager, settings_manager)
            state_manager = StateManager(key_manager, logger_manager)
            ui_manager = UiManager(root, state_manager)
            state_changed_event_polling_thread = Thread(target=ui_manager.state_changed_event_handler, args=(state_manager.state_changed_event,))
            state_error_event_polling_thread = Thread(target=ui_manager.state_error_event_handler, args=(state_manager.state_error_event,))
            state_changed_event_polling_thread.start()
            state_error_event_polling_thread.start()
            key_manager.start_listening()

            root.mainloop()

            key_manager.stop_listening()
            ui_manager.stop_event_listener_thread()
            if state_changed_event_polling_thread is not None and state_changed_event_polling_thread.is_alive():
                state_changed_event_polling_thread.join()
            if state_error_event_polling_thread is not None and state_error_event_polling_thread.is_alive():
                state_error_event_polling_thread.join()
            key_manager.stop_key_press()
            key_manager.release_pressed_keys()

        except Exception as e:
            logger_manager.log_error(e)
        finally:
            if root.winfo_exists():
                root.destroy()
finally:
    lock.release()
    sys.exit(0)