import json
import os

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        with open('rudra_config.json') as f:
            self.config = json.load(f)

    @property
    def wake_word(self):
        return self.config['assistant']['wake_word']

    @property
    def voice_rate(self):
        return self.config['assistant']['voice']['rate']

    @property
    def language(self):
        return self.config['user']['language']

    @property
    def voice_volume(self):
        return self.config['assistant']['voice']['volume']

    @property
    def recognition_settings(self):
        return self.config['assistant'].get('recognition', {
            'energy_threshold': 2000,
            'pause_threshold': 0.8,
            'dynamic_energy_ratio': 1.5,
            'adjust_ambient_duration': 0.5
        })