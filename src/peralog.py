import os
from pathlib import Path
import sys
from loguru import logger

from .commons import env_to_bool
from .constants import logdir_path


logdir = Path(logdir_path)
if not logdir.exists():
    os.mkdir(logdir)

stdout_level = "DEBUG" if env_to_bool(os.getenv("DEBUG")) else "WARNING"
file_level = "DEBUG" if env_to_bool(os.getenv("DEBUG")) else "INFO"

log_format = "{time}\t{message}"
logger.remove()
logger.add(sys.stdout, format=log_format, level=stdout_level, colorize=True, backtrace=True, diagnose=True)
logger.add(logdir.joinpath("peracotta.log"), format=log_format, level=file_level)
