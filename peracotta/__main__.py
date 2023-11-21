import os
import signal
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from PyQt6 import QtWidgets

import commons
from Ui import Ui

logdir_path = "logs"


@logger.catch()
def excepthook(exc_type, exc_value, exc_tb):
    critical_errors = []  # error classes that should crash the program

    QtWidgets.QMessageBox.warning(None, "Error", f"Peracotta encountered an exception ({exc_type.__name__}).\nSee the logs for the traceback.")

    if any([exc_type is exc_t for exc_t in critical_errors]):
        QtWidgets.QApplication.quit()

    raise exc_type(exc_value)  # doesn't close the program, but exits the function and shows up on the logs


sys.excepthook = excepthook
signal.signal(signal.SIGINT, signal.SIG_DFL)  # makes CTRL+C work

logdir = Path(logdir_path)
if not logdir.exists():
    os.mkdir(logdir)

stdout_level = "DEBUG" if commons.env_to_bool(os.getenv("DEBUG")) else "WARNING"
file_level = "DEBUG" if commons.env_to_bool(os.getenv("DEBUG")) else "INFO"

log_format = "{time}\t{message}"
logger.remove()
logger.add(sys.stdout, format=log_format, level=stdout_level, colorize=True, backtrace=True, diagnose=True)
logger.add(logdir.joinpath("peracotta.log"), format=log_format, level=file_level)

# noinspection PyBroadException
load_dotenv()
tarallo_url = os.environ["TARALLO_URL"]
tarallo_token = os.environ["TARALLO_TOKEN"]
app = QtWidgets.QApplication(sys.argv)
# This is EXTREMELY IMPORTANT, DON'T TACH [sic], DO NOT REMOVE IT EVER
# noinspection PyUnusedLocal
window = Ui(app, tarallo_url, tarallo_token)
app.exec()
