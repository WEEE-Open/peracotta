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

for dir in conf_dirs:
    if dir.exists():
        conf_dir = dir
        break


def load_conf():
    load_dotenv(dir.joinpath(".env"))


load_conf()

CONFIG = {
    "TARALLO_URL": os.environ["TARALLO_URL"],
    "TARALLO_TOKEN": os.environ["TARALLO_TOKEN"],
    "TARALLO_FEATURES_AUTO_DOWNLOAD": os.environ["TARALLO_FEATURES_AUTO_DOWNLOAD"],
    "GENERATE_FILES_USE_SUDO": os.environ["GENERATE_FILES_USE_SUDO"],
    "GENERATE_FILES_ASK_SUDO_PASSWORD": os.environ["GENERATE_FILES_ASK_SUDO_PASSWORD"],
}

logger.info(f"{conf_dir = }")
