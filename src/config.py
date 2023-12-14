import os
from pathlib import Path

from dotenv import load_dotenv

from .commons import env_to_bool

home_dir = Path().home()

conf_dir = home_dir.joinpath(".config/peracotta")


def load_conf():
    load_dotenv(conf_dir.joinpath(".env"))


load_conf()

CONFIG = {
    "TARALLO_URL": os.environ.get("TARALLO_URL", None),
    "TARALLO_TOKEN": os.environ.get("TARALLO_TOKEN", None),
    "TARALLO_FEATURES_AUTO_DOWNLOAD": env_to_bool(os.environ.get("TARALLO_FEATURES_AUTO_DOWNLOAD", "1")),
    "GENERATE_FILES_USE_SUDO": env_to_bool(os.environ.get("GENERATE_FILES_USE_SUDO", "1")),
    "GENERATE_FILES_ASK_SUDO_PASSWORD": env_to_bool(os.environ.get("GENERATE_FILES_ASK_SUDO_PASSWORD", "1")),
}
