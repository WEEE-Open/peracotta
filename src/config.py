import os
from pathlib import Path

import toml
from dotenv import load_dotenv

from .commons import parse_from_env

HOME_DIR = Path().home()

CONF_DIR = HOME_DIR.joinpath(".config/peracotta")
CONFIG = {}

keys = [
    "TARALLO_URL",
    "TARALLO_TOKEN",
    "TARALLO_FEATURES_AUTO_DOWNLOAD",
    "GENERATE_FILES_USE_SUDO",
    "GENERATE_FILES_ASK_SUDO_PASSWORD",
    "REPORT_URL",
    "AUTOMATIC_REPORT_ERRORS",
]

# 1) local environment
for key in keys:
    CONFIG[key] = parse_from_env(os.environ.get(key))

# 2) CONF_DIR's .env
try:
    load_dotenv(CONF_DIR.joinpath(".env"))
    for key in keys:
        if key not in CONFIG.keys() or CONFIG[key] is None:
            CONFIG[key] = parse_from_env(os.environ.get(key))
except FileNotFoundError:
    pass

# 3) CONF_DIR's toml
try:
    _toml_conf = toml.load(CONF_DIR.joinpath("config.toml"))
    for k in _toml_conf:
        if k not in CONFIG.keys() or CONFIG[k] is None:
            CONFIG[k] = _toml_conf[k]
except FileNotFoundError:
    pass

# 4) default toml
try:
    _toml_conf = toml.load(CONF_DIR.joinpath("config.toml"))
    for k in _toml_conf:
        if k not in CONFIG.keys() or CONFIG[k] is None:
            CONFIG[k] = _toml_conf[k]
except FileNotFoundError:
    pass
