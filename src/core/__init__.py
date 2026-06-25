# src/core/__init__.py
# Core package - contains app, config, and constants

from .app import SDFFMSApp
from .config import Config, get_config, set_config
from .constants import *