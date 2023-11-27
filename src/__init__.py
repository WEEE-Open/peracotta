import os
import signal
import sys
from pathlib import Path

from dotenv import load_dotenv
from PyQt6 import QtWidgets

from .gui import GUI
from .constants import logdir_path, VERSION
from .logger import logger, excepthook
from .commons import env_to_bool


def main_gui():
    if ["--version"] in sys.argv:
        print(f"P.E.R.A.C.O.T.T.A. Version {VERSION}")
        exit(0)

    if ["--logs"] in sys.argv:
        print(f"P.E.R.A.C.O.T.T.A.'s logs are located in {logdir_path}")
        exit(0)

    app = QtWidgets.QApplication(sys.argv)
    sys.excepthook = excepthook
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # makes CTRL+C work

    logdir = Path(logdir_path)
    if not logdir.exists():
        os.mkdir(logdir)

    stdout_level = "DEBUG" if env_to_bool(os.getenv("DEBUG")) else "WARNING"
    file_level = "DEBUG" if env_to_bool(os.getenv("DEBUG")) else "INFO"

    log_format = "{time}\t{message}"
    logger.remove()
    logger.add(sys.stdout, format=log_format, level=stdout_level, colorize=True, backtrace=True, diagnose=True)
    logger.add(logdir.joinpath("peracotta.log"), format=log_format, level=file_level)

    # noinspection PyBroadException
    load_dotenv()
    tarallo_url = os.environ["TARALLO_URL"]
    tarallo_token = os.environ["TARALLO_TOKEN"]
    # noinspection PyUnusedLocal
    window = GUI(app, tarallo_url, tarallo_token)
    app.exec()


def main_cli():
    print("Sorry, peracruda isn't implemented in v2 yet! Use the old one at https://github.com/WEEE-Open/peracotta")
