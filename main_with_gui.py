#!/usr/bin/gksu /usr/bin/python3

import sys, os, subprocess as sp
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QLabel, QWidget, QMessageBox
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from extract_data import extract_and_collect_data_from_generated_files
from itertools import chain


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
        self.generate_files_button.clicked.connect(lambda: self.prompt_has_dedicated_gpu(window))

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

    def prompt_has_dedicated_gpu(self, window: QMainWindow):
        while True:
            answer = QMessageBox.question(self, "Discrete GPU",
                                          "Does this system have a dedicated video card?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if answer == QMessageBox.Yes:
                confirm = QMessageBox.question(self, "Confirm",
                                               "Do you confirm this system has a dedicated video card?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    self.generate_files(window, has_dedicated_gpu=True)
                    break
                else:
                    continue
            else:
                confirm = QMessageBox.question(self, "Confirm",
                                               "Do you confirm this system has an integrated GPU?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    self.generate_files(window, has_dedicated_gpu=False)
                    break
                else:
                    continue

    def generate_files(self, window: QMainWindow, has_dedicated_gpu: bool):
        try:
            working_directory = sp.check_output(["pwd"])[:-1].decode("ascii")
            if not os.path.isdir(working_directory + "/tmp"):
                os.makedirs(working_directory + "/tmp")

            folder_name = "tmp"
            path_to_gen_files_sh = working_directory + "/generate_files.sh"
            with sp.Popen(["sudo", path_to_gen_files_sh, folder_name], shell=False) as process:
                process.wait(timeout=10)
            # the line below is needed in order to not close the window!
            window.takeCentralWidget()
            new_widget = FilesGenerated(window, has_dedicated_gpu)
            window.setCentralWidget(new_widget)

        except sp.CalledProcessError as err:
            QMessageBox.critical(self, "Error", "Something went wrong while running 'generate_files.sh'. Here is the stderr:\n" + err.output)

        except FileNotFoundError:
            QMessageBox.warning(self, "Warning", "I couldn't find the 'generate_files.sh' script in the current directory. Please import it and try again.")

        except Exception as e:
            QMessageBox.critical(self, "WTF1", "Have a look at the extent of your huge fuck-up:\n" + str(e))


class FilesGenerated(QWidget):
    def __init__(self, window: QMainWindow, has_dedicated_gpu: bool):
        super().__init__()
        self.init_ui(window, has_dedicated_gpu)

    def init_ui(self, window: QMainWindow, has_dedicated_gpu: bool):
        self.label = QLabel("Everything went fine. Click the button below if you want to proceed with the data extraction.\n"
                            "You will be able to review the data after this process.")
        self.extract_data_button = QPushButton("Extract data from output files")
        self.extract_data_button.clicked.connect(lambda: self.extract_data_from_generated_files(window, has_dedicated_gpu))

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.extract_data_button)
        h_box.addStretch()

        v_box = QVBoxLayout()
        v_box.addWidget(self.label)
        v_box.addSpacing(15)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

    def extract_data_from_generated_files(self, window: QMainWindow, has_dedicated_gpu: bool):
        try:
            system_info = extract_and_collect_data_from_generated_files(has_dedicated_gpu)
            print(system_info)
            # flatten system_info (list of list of dicts to list of dicts)
            flattened_system_info = chain.from_iterable(system_info)
            print(flattened_system_info)
            window.takeCentralWidget()
            new_widget = VerifyExtractedData(window, flattened_system_info)
            window.setCentralWidget(new_widget)

        # TODO: fix that the print() calls above don't work, and the window closes immediately after clicking "generate files", without spawning the dialog box of the except below
        except Exception as e:
            QMessageBox.critical(self, "WTF2", "Have a look at the extent of your huge fuck-up:\n" + str(e))


class VerifyExtractedData(QWidget):
    def __init__(self, window: QMainWindow, system_info):
        super().__init__()
        self.init_ui(window, system_info)

    def init_ui(self, window: QMainWindow, system_info):

        v_box = QVBoxLayout()

        # if system_info is empty
        if not system_info:
            nothing_found = QLabel("Nothing was found.")
            v_box.addWidget(nothing_found)

        # TODO: fix "string indices must be integers" - not an error anymore (?)
        for i, component in enumerate(system_info):
            if i == 0:
                prev_type = component["type"]
            else:
                prev_type = system_info[i-1]["type"]

            if component["type"] != prev_type or i == 0:
                title = QLabel(component["type"].upper())
                title.setFont(QFont("futura", pointSize=16, italic=False))
                if i != 0:
                    v_box.addSpacing(10)
                v_box.addWidget(title)

            for feature in component.items():
                if feature[0] != "type":
                    h_box = QHBoxLayout()

                    # the single dict entry is converted to a tuple
                    name = QLabel(str(feature[0]))
                    if feature[1] != "":
                        # skip not human readable frequency and capacity
                        if feature[0] == "frequency" or feature[0] == "capacity":
                            continue
                        elif feature[0] == "human_readable_frequency":
                            name = QLabel("frequency")
                        elif feature[0] == "human_readable_capacity":
                            name = QLabel("capacity")
                        desc = QLabel(str(feature[1]))
                    else:
                        desc = QLabel("missing feature")
                        name.setStyleSheet("color: yellow")
                        desc.setStyleSheet("color: yellow")

                    h_box.addWidget(name)
                    h_box.addStretch()
                    h_box.addWidget(desc)

                    v_box.addLayout(h_box)

            v_box.addSpacing(15)

        self.setLayout(v_box)

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