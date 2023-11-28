import os
import signal
import sys

from PyQt6 import QtWidgets

from .commons import env_to_bool
from .config import CONFIG
from .constants import VERSION
from .gui import GUI
from .peralog import excepthook, logger, logdir_path
from . import peracruda


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

    tarallo_url = os.environ["TARALLO_URL"]
    tarallo_token = os.environ["TARALLO_TOKEN"]
    # noinspection PyUnusedLocal
    window = GUI(app, CONFIG["TARALLO_URL"], CONFIG["TARALLO_TOKEN"])
    app.exec()


def main_cli():
    print("Sorry, peracruda isn't implemented in v2 yet! Use the old one at https://github.com/WEEE-Open/peracotta")
    # peracruda.main_()
