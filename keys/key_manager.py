from pynput.keyboard import Controller, Key
from threading import Thread, Lock
import random, time
from keys.key_constants import keys, key_mapping

keyboard = Controller()

class KeyManager:
    def __init__(self, logger_manager):
        self.logger_manager = logger_manager
        self.has_started = False
        self.thread = None
        self.keys = keys
        self.key_mapping = key_mapping
        self.lock = Lock()
        self.pressed_keys = set()

    def validate_key(self, key):
        return key in keys

    def press_key(self, key, interval, alt_tab, random_delay):
        try:
            actual_key = key_mapping.get(key, key)
            while self.has_started:
                keyboard.tap(actual_key)
                if alt_tab:
                    with keyboard.pressed(Key.alt):
                        self.pressed_keys.add(Key.alt)
                        keyboard.tap(Key.tab)
                    self.pressed_keys.remove(Key.alt)

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
            self.logger_manager.log_error(e)

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
            self.logger_manager.log_error(e)

    def stop_key_press(self):
        with self.lock:
            self.has_started = False
            
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()

    def release_pressed_keys(self):
        for key in self.pressed_keys:
            try:
                keyboard.release(key)
            except Exception as e:
                self.logger_manager.log_error(e)
        self.pressed_keys.clear()