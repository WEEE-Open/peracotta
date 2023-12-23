import toml
import os
from pathlib import Path

from dotenv import load_dotenv

from .commons import parse_from_env

home_dir = Path().home()

conf_dir = home_dir.joinpath(".config/peracotta")
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

# 2) conf_dir's .env
try:
    load_dotenv(conf_dir.joinpath(".env"))
    for key in keys:
        if key not in CONFIG.keys() or CONFIG[key] is None:
            CONFIG[key] = parse_from_env(os.environ.get(key))
except FileNotFoundError:
    pass

# 3) conf_dir's toml
try:
    _toml_conf = toml.load(conf_dir.joinpath("config.toml"))
    for k in _toml_conf:
        if k not in CONFIG.keys() or CONFIG[k] is None:
            CONFIG[k] = _toml_conf[k]
except FileNotFoundError:
    pass

# 4) default toml
try:
    _toml_conf = toml.load(conf_dir.joinpath("config.toml"))
    for k in _toml_conf:
        if k not in CONFIG.keys() or CONFIG[k] is None:
            CONFIG[k] = _toml_conf[k]
except FileNotFoundError:
    pass
