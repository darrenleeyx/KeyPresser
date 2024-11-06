import os, yaml
import sys

class SettingsManager:
    def __init__(self):
        self.settings = self.get_settings()
        self.key_bindings = self.settings['key_bindings']

    def get_settings(self):
        settings_dir = '__settings__'
        settings_file_path = f'{settings_dir}\settings.yaml'

        if not os.path.exists(settings_file_path):
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir, exist_ok=True)
            self.create_default_settings_file(settings_file_path)

        with open(settings_file_path, 'r') as settings_file:
            return yaml.safe_load(settings_file)

    def create_default_settings_file(self, file_path):
        default_settings = yaml.safe_load("""
        key_bindings:
        - bind_from:
        - f8
        bind_to:
        - ctrl
        - c
        enabled: true
        name: copy
        - bind_from:
        - f9
        bind_to:
        - ctrl
        - v
        enabled: true
        name: paste
        """)
        with open(file_path, 'w') as settings_file:
            yaml.safe_dump(default_settings, settings_file)