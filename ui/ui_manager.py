from tkinter import ttk, font as tkFont
import tkinter as tk
import ui.ui_constants as ui_const
import constants as const
import keys.key_constants as key_const
from state.state import State
import time

class UiManager:
    def __init__(self, root, state_manager):
        self.root = root
        self.state_manager = state_manager
        self.start_button = None
        self.stop_event_listener = False
        self.setup_ui()

    def setup_ui(self):
        self.root.title(ui_const.APP_TITLE)
        icon = tk.PhotoImage(file=ui_const.ICON_PATH)
        self.root.iconphoto(False, icon)
        style = ttk.Style(self.root)
        style.theme_use(ui_const.APP_THEME)
        app_font = tkFont.Font(family=ui_const.APP_FONT, size=ui_const.APP_FONT_SIZE)
        style.configure('TLabel', font=app_font)
        style.configure('TButton', font=app_font)
        style.configure('TCheckbutton', font=app_font)
        style.configure('TEntry', font=app_font)
        style.configure('TCombobox', font=app_font)
        form_frame = ttk.Frame(self.root, padding=(0, 0))
        form_frame.pack(padx=5, pady=5)
        self.setup_form(form_frame)
        self.root.resizable(False, False)

    def setup_form(self, form_frame):
        key_label = ttk.Label(form_frame, text="Key:")
        key_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.key_var = tk.StringVar(value='a')
        key_combobox = ttk.Combobox(form_frame, textvariable=self.key_var, values=key_const.keys)
        key_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        interval_label = ttk.Label(form_frame, text="Interval (milliseconds):")
        interval_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.interval_var = tk.StringVar(value='1000')
        interval_entry = ttk.Entry(form_frame, textvariable=self.interval_var)
        interval_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.alt_tab_var = tk.BooleanVar()
        alt_tab_checkbox = ttk.Checkbutton(form_frame, text="Press Alt+Tab after key press", variable=self.alt_tab_var)
        alt_tab_checkbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.random_delay_var = tk.BooleanVar()
        random_delay_checkbox = ttk.Checkbutton(form_frame, text="Random delay after key press", variable=self.random_delay_var)
        random_delay_checkbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.start_button = ttk.Button(form_frame, text="Start", command=lambda: self.state_manager.toggle_state(self.key_var.get(), self.interval_var.get(), const.MIN_INTERVAL_MS, self.alt_tab_var.get(), self.random_delay_var.get()))
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

    def update_start_button_text(self, text):
        if self.start_button:
            self.start_button.config(text=text)

    def wait_for_state_changed_event(self, event):
        while not self.stop_event_listener:
            state = event.wait() 
            if state == State.STARTED:
                self.update_start_button_text("Stop")
            elif state == State.STOPPED:
                self.update_start_button_text("Start")
            event.clear()
            time.sleep(5/1000)

    def stop_event_listener_thread(self):
        self.stop_event_listener = True