from pynput.keyboard import Controller, Key
from tkinter import messagebox
from threading import Thread, Lock
import random
import time
import logging
from keys.key_constants import keys, key_mapping

keyboard = Controller()

class KeyManager:
    def __init__(self):
        self.has_started = False
        self.thread = None
        self.keys = keys
        self.key_mapping = key_mapping
        self.lock = Lock()

    def validate_key(self, key):
        if key not in keys:
            messagebox.showerror("Invalid Key", f"The key '{key}' is not valid.")
            return False
        return True

    def press_key(self, key, interval, alt_tab, random_delay):
        try:
            actual_key = key_mapping.get(key, key)
            while self.has_started:
                keyboard.tap(actual_key)
                if alt_tab:
                    with keyboard.pressed(Key.alt):
                        keyboard.tap(Key.tab)
                        
                total_sleep_time = 0
                while total_sleep_time < interval and self.has_started:
                    sleep_time = min(0.1, interval - total_sleep_time)  # Sleep in smaller increments
                    time.sleep(sleep_time)
                    total_sleep_time += sleep_time
                if random_delay:
                    total_sleep_time = 0
                    random_interval = random.uniform(interval - 0.02, interval + 0.02)
                    while total_sleep_time < random_interval and self.has_started:
                        sleep_time = min(0.1, random_interval - total_sleep_time)
                        time.sleep(sleep_time)
                        total_sleep_time += sleep_time
        except Exception as e:
            logging.error(f"Error in press_key: {e}")

    def start_key_press(self, key, interval_ms, min_interval_ms, should_alt_tab, should_random_delay):
        if not self.validate_key(key):
            return
        
        with self.lock:
            self.has_started = True

        try:
            interval = max(min_interval_ms, int(interval_ms)) / 1000
            self.thread = Thread(target=self.press_key, args=(key, interval, should_alt_tab, should_random_delay))
            self.thread.start()
        except Exception as e:
            logging.error(f"Error in start_key_press: {e}")
            messagebox.showerror("Error", "An error occurred while starting the key press.")

    def stop_key_press(self):
        with self.lock:
            self.has_started = False
            
        if self.thread.is_alive():
            self.thread.join()

    def release_keys(self):
        for key in key_mapping.values():
            try:
                keyboard.release(key)
            except Exception as e:
                logging.error(f"Error releasing key {key}: {e}")

key_manager = KeyManager()