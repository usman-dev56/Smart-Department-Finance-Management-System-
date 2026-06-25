# src/core/config.py
"""Application configuration"""
import os
import json

CONFIG_FILE = os.path.join("data", "config.json")

DEFAULTS = {
    "db_path": os.path.join("data", "database", "dffms.db"),
    "schema_path": "src/database/schema.sql",
    "theme": "dark",
    "color_theme": "blue",
    "currency_symbol": "PKR",
    "window_width": 1280,
    "window_height": 780,
    "min_window_width": 1024,
    "min_window_height": 768,
    "receipt_prefix": "DEPT",
    "log_level": "INFO",
}

# ─── Application Constants (Added for app.py) ──────────────────────────────

APP_TITLE = "Smart Department Finance & Fund Management System"
APP_VERSION = "1.0.0"
WINDOW_SIZE = "1280x780"
MIN_WINDOW_SIZE = (1024, 768)
DB_PATH = os.path.join("data", "database", "dffms.db")
SCHEMA_PATH = "src/database/schema.sql"
DEFAULT_THEME = "dark"
DEFAULT_COLOR = "blue"


class Config:
    _data = None

    @classmethod
    def load(cls):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                cls._data = {**DEFAULTS, **json.load(f)}
        else:
            cls._data = dict(DEFAULTS)
            cls.save()
        return cls._data

    @classmethod
    def get(cls, key, default=None):
        if cls._data is None:
            cls.load()
        return cls._data.get(key, default)

    @classmethod
    def set(cls, key, value):
        if cls._data is None:
            cls.load()
        cls._data[key] = value
        cls.save()

    @classmethod
    def save(cls):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(cls._data, f, indent=2)


# Shortcut functions
def get_config(key, default=None):
    return Config.get(key, default)


def set_config(key, value):
    return Config.set(key, value)