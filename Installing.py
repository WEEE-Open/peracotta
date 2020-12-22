from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMovie
import sys
import os


class UIMainWindow(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__()
        self.main_window = main_window
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.label = QtWidgets.QLabel(self.central_widget)
        self.movie = QMovie(os.path.join("data", "Installing.gif"))
        self.setup_ui()

    def setup_ui(self):
        self.main_window.setObjectName("main_window")
        self.main_window.resize(400, 200)
        self.central_widget.setObjectName("central_widget")
        self.label.setGeometry(QtCore.QRect(0, 0, 400, 200))
        self.label.setMinimumSize(QtCore.QSize(400, 200))
        self.label.setMaximumSize(QtCore.QSize(400, 200))
        self.label.setObjectName("label")
        self.main_window.setCentralWidget(self.central_widget)
        self.label.setMovie(self.movie)
        self.movie.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = UIMainWindow(window)
    window.show()
    sys.exit(app.exec_())
