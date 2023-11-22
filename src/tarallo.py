import pytarallo.Errors
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from pytarallo import Tarallo

from .constants import PATH


class Uploader(QtCore.QThread):
    successEvent = QtCore.pyqtSignal(str)
    failureEvent = QtCore.pyqtSignal(str, str)

    def __init__(
        self,
        data: list[dict],
        tarallo_url: str,
        tarallo_token: str,
        bulk_identifier: str,
        overwrite: bool,
    ):
        super().__init__()
        self.data = data
        self.tarallo_url = tarallo_url
        self.tarallo_token = tarallo_token
        self.bulk_identifier = bulk_identifier
        self.overwrite = overwrite

    def run(self) -> None:
        try:
            tarallo = Tarallo.Tarallo(self.tarallo_url, self.tarallo_token)
            ver = tarallo.bulk_add(self.data, self.bulk_identifier, self.overwrite)
            if ver:
                # TODO: use generated identifier if none was provided
                self.successEvent.emit(self.bulk_identifier)
            else:
                self.failureEvent.emit("cannot_upload", self.bulk_identifier)

        except pytarallo.Errors.NoInternetConnectionError:
            self.failureEvent.emit("cannot_reach", self.bulk_identifier)


class TaralloUploadDialog(QtWidgets.QDialog):
    signal = QtCore.pyqtSignal(bool, str, name="event")

    def __init__(self, parent: QtWidgets.QMainWindow, bulk_id: str = ""):
        super().__init__(parent)
        uic.loadUi(PATH["TARALLOUPLOADDIALOG"], self)

        self.setWindowTitle("Set bulk identifier")
        self.bulkLineEdit = self.findChild(QtWidgets.QLineEdit, "bulkLineEdit")
        self.bulkLineEdit.setText(bulk_id)
        self.okButton = self.findChild(QtWidgets.QPushButton, "okButton")
        self.okButton.clicked.connect(self.ok_signal)
        self.cancelButton = self.findChild(QtWidgets.QPushButton, "cancelButton")
        self.cancelButton.clicked.connect(self.cancel_signal)
        self.overwriteCheckBox = self.findChild(QtWidgets.QCheckBox, "overwriteCheckBox")
        self.show()

    def ok_signal(self):
        self.signal.emit(self.overwriteCheckBox.isChecked(), self.bulkLineEdit.text())
        self.close()

    def cancel_signal(self):
        self.close()


def tarallo_success_dialog(url: str):
    dialog: QtWidgets.QMessageBox = QtWidgets.QMessageBox(
        QtWidgets.QMessageBox.Icon.Information,
        "Upload successful",
        "Upload successful! Now go to TARALLO and finish the job.",
    )
    std_width = QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MessageBoxWarning).availableSizes()[-1].width()
    dialog.setIconPixmap(QtGui.QPixmap(PATH["ICON"]).scaledToWidth(std_width, QtCore.Qt.TransformationMode.SmoothTransformation))
    dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
    view_on_tarallo_button = dialog.addButton("View on TARALLO", dialog.ButtonRole.ActionRole)
    dialog.exec()
    if dialog.clickedButton() == view_on_tarallo_button:
        url = QtCore.QUrl(url)
        if not QtGui.QDesktopServices.openUrl(url):
            QtWidgets.QMessageBox.warning(dialog, "Cannot Open Url", f"Could not open url {url}")
        return True
    return False
