"""
Peracotta is configurable in various ways.
The reccomended is with the file `~/.config/WEEE Open/peracotta/config.toml`.

Example config:
```toml
TARALLO_URL = "http://192.168.2.142:8080"
TARALLO_TOKEN = "yoLeCHmEhNNseN0BlG0s3A:ksfPYziGg7ebj0goT0Zc7pbmQEIYvZpRTIkwuscAM_k"
TARALLO_FEATURES_AUTO_DOWNLOAD = false

GENERATE_FILES_USE_SUDO = true
GENERATE_FILES_ASK_SUDO_PASSWORD = true

AUTOMATIC_REPORT_ERRORS = true
REPORT_URL = "http://127.0.0.1:9999"
```
This configuration can be overridden by `~/.config/WEEE Open/peracotta/.env`
and/or environment variables. If both are used, the latter take precedence.

For compatibility with the old M.I.S.O.'s martello.sh script, it's also possible to configure it by placing a .env file in the src directory. For the same reasons, there's a .env.example in the source code at the appropriate place
"""
import os
from pathlib import Path

import toml
from dotenv import load_dotenv

from .commons import parse_from_env

HOME_DIR = Path().home()

CONF_DIR = HOME_DIR.joinpath(".config/WEEE Open/peracotta")
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

# 1.1) src's .env, for compatibility with old M.I.S.O.
try:
    load_dotenv(".env")
    for key in keys:
        if key not in CONFIG.keys() or CONFIG[key] is None:
            CONFIG[key] = parse_from_env(os.environ.get(key))
except FileNotFoundError:
    pass

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
