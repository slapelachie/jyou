"""Default settings"""
import os.path

APP_NAME = "jyou"
DEBUG_MODE = False

if "XDG_DATA_HOME" in os.environ:
    DATA_PATH = os.path.join(os.getenv("XDG_DATA_HOME"), APP_NAME)
else:
    DATA_PATH = os.path.expanduser("~/.local/share/" + APP_NAME)

if "XDG_CONFIG_HOME" in os.environ:
    CONFIG_PATH = os.path.join(os.getenv("XDG_CONFIG_HOME"), APP_NAME)
else:
    CONFIG_PATH = os.path.expanduser("~/.config/" + APP_NAME)

if "XDG_CACHE_HOME" in os.environ:
    CACHE_PATH = os.path.join(os.getenv("XDG_CACHE_HOME"), APP_NAME)
else:
    CACHE_PATH = os.path.expanduser("~/.cache/" + APP_NAME)
