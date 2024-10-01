import os
import sys
from pathlib import Path

from loguru import logger

from .config import CONF_DIR

logdir = Path(CONF_DIR).joinpath("logs")
if not logdir.exists():
    os.makedirs(logdir)

try:
    DEBUG = sys.argv[1] == "DEBUG"
except IndexError:
    DEBUG = False

stdout_level = "DEBUG" if DEBUG else "WARNING"
file_level = "DEBUG" if DEBUG else "INFO"

log_format = "{time}\t{message}"
logger.remove()
logger.add(sys.stdout, format=log_format, level=stdout_level, colorize=True, backtrace=True, diagnose=True)
logger.add(logdir.joinpath("peracotta.log"), format=log_format, level=file_level)

# logger.info(f"{CONF_DIR = }")
