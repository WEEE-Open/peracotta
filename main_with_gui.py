#!/usr/bin/gksu /usr/bin/python3

import sys, os, subprocess as sp
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QLabel, QWidget, QMessageBox
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from extract_data import extract_and_collect_data_from_generated_files


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        welcome_widget = Welcome(self)
        self.setCentralWidget(welcome_widget)
        self.setWindowTitle("P.E.R.A.C.O.T.T.A.")
        self.setWindowIcon(QIcon("pear_emoji.png"))

        self.show()


class Welcome(QWidget):
    def __init__(self, window: QMainWindow):
        super().__init__()
        self.init_ui(window)

    def init_ui(self, window: QMainWindow):
        self.title = QLabel("Welcome to P.E.R.A.C.O.T.T.A.")
        self.subtitle = QLabel("(Progetto Esteso Raccolta Automatica Configurazioni hardware Organizzate Tramite Tarallo Autonomamente)")
        self.intro = QLabel("When you're ready to generate the files required to gather info about this system, click the 'Generate files' button below.")

        title_font = QFont("futura", pointSize=24, italic=False)
        subtitle_font = QFont("futura", pointSize=14, italic=True)
        self.title.setFont(title_font)
        self.subtitle.setFont(subtitle_font)

        self.generate_files_button = QPushButton("Generate Files")
        self.generate_files_button.clicked.connect(lambda: self.generate_files(window))

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.generate_files_button)
        h_box.addStretch()

        v_box = QVBoxLayout()
        v_box.addWidget(self.title)
        v_box.addWidget(self.subtitle)
        v_box.addSpacing(30)
        v_box.addWidget(self.intro)
        v_box.addSpacing(15)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

    def generate_files(self, window: QMainWindow):
        try:
            working_directory = sp.check_output(["pwd"])
            path_to_gen_files_sh = working_directory[:-1].decode("ascii") + "/generate_files.sh"
            with sp.Popen(["sudo", path_to_gen_files_sh], shell=False) as process:
                process.wait(timeout=10)
            # the line below is needed in order to not close the window!
            window.takeCentralWidget()
            new_widget = FilesGenerated(window)
            window.setCentralWidget(new_widget)

        except sp.CalledProcessError as err:
            QMessageBox.critical(self, "Error", "Something went wrong while running 'generate_files.sh'. Here is the stderr:\n" + err.output)

        except FileNotFoundError:
            QMessageBox.warning(self, "Warning", "I couldn't find the 'generate_files.sh' script in the current directory. Please import it and try again.")

        except Exception as e:
            QMessageBox.critical(self, "WTF", "Have a look at the extent of your huge fuck-up:\n" + str(e))


class FilesGenerated(QWidget):
    def __init__(self, window: QMainWindow):
        super().__init__()
        self.init_ui(window)

    def init_ui(self, window: QMainWindow):
        self.label = QLabel("Everything went fine. Click the button below if you want to proceed with the data extraction.\n"
                            "You will be able to review the data after this process.")
        self.extract_data_button = QPushButton("Extract data from output files")
        self.extract_data_button.clicked.connect(lambda: self.extract_data_from_generated_files(window))

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.extract_data_button)
        h_box.addStretch()

        v_box = QVBoxLayout()
        v_box.addWidget(self.label)
        v_box.addSpacing(15)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

    def extract_data_from_generated_files(self, window: QMainWindow):
        try:
            system_info = extract_and_collect_data_from_generated_files()
            window.takeCentralWidget()
            new_widget = VerifyExtractedData(window, system_info)
            window.setCentralWidget(new_widget)

        except Exception as e:
            QMessageBox.critical(self, "WTF", "Have a look at the extent of your huge fuck-up:\n" + str(e))


class VerifyExtractedData(QWidget):
    def __init__(self, window: QMainWindow, system_info):
        super().__init__()
        self.init_ui(window, system_info)

    def init_ui(self, window: QMainWindow, system_info):
        pass
    # TODO: OwO *notices beautifully displayed gathered system info*


def main():
    app = QApplication(sys.argv)

    # set SUPERIOR dark theme
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(15, 15, 15))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(palette)
    Window()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()