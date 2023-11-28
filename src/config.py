import os
from pathlib import Path

from dotenv import load_dotenv

from .constants import basedir
from .peralog import logger

home_dir = Path().home()
conf_dirs = [
    home_dir.joinpath(".config/peracotta"),
    home_dir.joinpath("peracotta"),
    Path("/etc/peracotta"),
    basedir,
]

for c_dir in conf_dirs:
    if c_dir.exists():
        conf_dir = c_dir
        break


def load_conf():
    load_dotenv(conf_dir.joinpath(".env"))


load_conf()

CONFIG = {
    "TARALLO_URL": os.environ.get(["TARALLO_URL"], None),
    "TARALLO_TOKEN": os.environ.get(["TARALLO_TOKEN"], None),
    "TARALLO_FEATURES_AUTO_DOWNLOAD": env_to_bool(os.environ.get(["TARALLO_FEATURES_AUTO_DOWNLOAD"], "1")),
    "GENERATE_FILES_USE_SUDO": env_to_bool(os.environ.get(["GENERATE_FILES_USE_SUDO"], "1")),
    "GENERATE_FILES_ASK_SUDO_PASSWORD": env_to_bool(os.environ.get(["GENERATE_FILES_ASK_SUDO_PASSWORD"], "1")),
}

logger.info(f"{conf_dir = }")
