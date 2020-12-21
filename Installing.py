from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QMovie
import sys
import os

class Ui_MainWindow(QWidget):
    def setupUi(self,MainWindow):
        super().__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400,200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0,0,400,200))
        self.label.setMinimumSize(QtCore.QSize(400,200))
        self.label.setMaximumSize(QtCore.QSize(400,200))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.movie = QMovie(os.path.join("data","Installing.gif"))
        self.label.setMovie(self.movie)
        self.movie.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())