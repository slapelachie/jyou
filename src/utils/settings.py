import os.path

app_name = "jyou"

if "XDG_DATA_HOME" in os.environ:
	DATA_PATH = os.path.join(os.getenv("XDG_DATA_HOME"), app_name)
else:
	DATA_PATH = os.path.expanduser('~/.local/share/'+app_name)

if "XDG_CONFIG_HOME" in os.environ:
	CONFIG_PATH = os.path.join(os.getenv("XDG_CONFIG_HOME"), app_name)
else:
	CONFIG_PATH = os.path.expanduser('~/.config/'+app_name)

if "XDG_CACHE_HOME" in os.environ:
	CACHE_PATH = os.path.join(os.getenv("XDG_CACHE_HOME"), app_name)
else:
	CACHE_PATH = os.path.expanduser('~/.cache/'+app_name)

DEBUG_MODE = False