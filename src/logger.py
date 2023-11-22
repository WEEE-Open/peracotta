from loguru import logger
from PyQt6 import QtWidgets


@logger.catch()
def excepthook(exc_type, exc_value, exc_tb):
    critical_errors = []  # error classes that should crash the program

    QtWidgets.QMessageBox.warning(None, "Error", f"Peracotta encountered an exception ({exc_type.__name__}).\nSee logs for the traceback.")

    if any([exc_type is exc_t for exc_t in critical_errors]):
        QtWidgets.QApplication.quit()

    # This two lines are for pretty printing traceback with color and additional info.
    options = ((exc_type, exc_value, exc_tb),) + logger._options[1:]
    logger._log("ERROR", False, options, "", None, None)
