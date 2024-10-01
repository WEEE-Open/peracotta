from PyQt5 import QtWidgets

from ..peralog import logger
from .exceptions import MissingFeaturesError

critical_errors = [MissingFeaturesError]  # error classes that should crash the program


def errored():
    return _errored


_errored = False


def gui_excepthook(exc_type, exc_value, exc_tb):
    """Custom exception handler for peracotta's GUI version

    Args:
        exc_type: exception type
        exc_value: exception value
        exc_tb: exception traceback
    """
    global _errored
    _errored = True

    QtWidgets.QMessageBox.warning(
        None,
        "Error",
        f"Peracotta encountered an exception ({exc_type.__name__}).\nSee logs for the traceback.",
    )
    if any([exc_type is exc_t for exc_t in critical_errors]):
        logger.error("Encountered a critical error")
        QtWidgets.QApplication.quit()

    # These two lines are for pretty printing traceback with color
    # and additional info.
    # This is loguru syntax and should be modified if the logging system is changed
    options = ((exc_type, exc_value, exc_tb),) + logger._options[1:]
    logger._log("ERROR", False, options, "", None, None)
    # if CONFIG["AUTOMATIC_REPORT_ERRORS"] and not send_crash_notification():
    #     logger.info("Couldn't upload crash log.")
