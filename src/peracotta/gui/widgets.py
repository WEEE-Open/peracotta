import json
from cgitb import text
from typing import List

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from ..constants import PATH


class JsonWidget(QtWidgets.QDialog):
    def __init__(self, data: List[dict], window_size: QtCore.QSize):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        text_edit = QtWidgets.QPlainTextEdit()
        text_edit = QtWidgets.QTextEdit()
        text_edit.setWordWrapMode(QtGui.QTextOption.WrapMode.NoWrap)
        text_edit.setPlainText(f"{json.dumps(data, indent=2)}")
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        self.setLayout(layout)
        new_size = QtCore.QSize(int(window_size.width() * 0.8), int(window_size.height() * 0.8))
        self.resize(new_size)
        self.exec()


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QMainWindow, title: str, detailed_error: str):
        super().__init__(parent)
        pass
        uic.loadUi(PATH["ERRORDIALOG"], self)
        self.setWindowTitle("Error")
        self.iconLabel = self.findChild(QtWidgets.QLabel, "iconLabel")
        self.textLabel = self.findChild(QtWidgets.QLabel, "textLabel")
        self.textLabel.setText(title)
        self.errorTextEdit = self.findChild(QtWidgets.QPlainTextEdit, "errorTextEdit")
        self.errorTextEdit.setPlainText(detailed_error)
        self.show()
