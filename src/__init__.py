import os
import signal
import sys

from PyQt6 import QtWidgets

from . import peracruda
from .commons import env_to_bool
from .config import CONFIG
from .constants import VERSION
from .gui import GUI, gui_excepthook
from .peralog import logdir_path, logger


def common_args_parsing():
    """Parse arguments common to both GUI and CLI version
    --version prints the current version and quits.
    --logs prints the path where logs are stored and quits.
    """
    if ["--version"] in sys.argv:
        print(f"P.E.R.A.C.O.T.T.A. Version {VERSION}")
        exit(0)

    if ["--logs"] in sys.argv:
        print(f"P.E.R.A.C.O.T.T.A.'s logs are located in {logdir_path}")
        exit(0)


def main_gui():
    common_args_parsing()

    app = QtWidgets.QApplication(sys.argv)
    sys.excepthook = gui_excepthook
    # makes CTRL+ C work
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # noinspection PyUnusedLocal
    window = GUI(app)
    app.exec()
    logger.info("Started PERACOTTA")


def main_cli():
    print("Sorry, peracruda isn't implemented in v2 yet! Use the old one at https://github.com/WEEE-Open/peracotta")
    common_args_parsing()
    # peracruda.main_()
