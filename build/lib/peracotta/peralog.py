import os
import sys
from pathlib import Path

from loguru import logger

from .commons import env_to_bool
from .config import CONF_DIR

logdir = Path(CONF_DIR).joinpath("logs")
if not logdir.exists():
    os.makedirs(logdir)

stdout_level = "DEBUG" if env_to_bool(os.getenv("DEBUG")) else "WARNING"
file_level = "DEBUG" if env_to_bool(os.getenv("DEBUG")) else "INFO"

log_format = "{time}\t{message}"
logger.remove()
logger.add(sys.stdout, format=log_format, level=stdout_level, colorize=True, backtrace=True, diagnose=True)
logger.add(logdir.joinpath("peracotta.log"), format=log_format, level=file_level)

logger.info(f"{CONF_DIR = }")
