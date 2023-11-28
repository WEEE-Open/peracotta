import os
from pathlib import Path
import sys
from loguru import logger
from PyQt6 import QtWidgets

from .commons import env_to_bool
from .constants import logdir_path


@logger.catch()
def excepthook(exc_type, exc_value, exc_tb):
    critical_errors = []  # error classes that should crash the program

    QtWidgets.QMessageBox.warning(None, "Error", f"Peracotta encountered an exception ({exc_type.__name__}).\nSee logs for the traceback.")

    if any([exc_type is exc_t for exc_t in critical_errors]):
        QtWidgets.QApplication.quit()

    # This two lines are for pretty printing traceback with color and additional info.
    options = ((exc_type, exc_value, exc_tb),) + logger._options[1:]
    logger._log("ERROR", False, options, "", None, None)


logdir = Path(logdir_path)
if not logdir.exists():
    os.mkdir(logdir)

stdout_level = "DEBUG" if env_to_bool(os.getenv("DEBUG")) else "WARNING"
file_level = "DEBUG" if env_to_bool(os.getenv("DEBUG")) else "INFO"

log_format = "{time}\t{message}"
logger.remove()
logger.add(sys.stdout, format=log_format, level=stdout_level, colorize=True, backtrace=True, diagnose=True)
logger.add(logdir.joinpath("peracotta.log"), format=log_format, level=file_level)
