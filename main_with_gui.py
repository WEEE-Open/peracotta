import sys, os, subprocess as sp
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QLabel, QWidget, QMessageBox
from PyQt5.QtGui import QFont


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        welcome_widget = Welcome(self)
        self.setCentralWidget(welcome_widget)
        self.setWindowTitle("P.E.R.A.C.O.T.T.A.")

        self.show()

    def next_clicked(self):
        pass


class Welcome(QWidget):
    def __init__(self, window:QMainWindow):
        super().__init__()
        self.init_ui(window)

    def init_ui(self, window:QMainWindow):
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

    # TODO: fix when dmidecode, lscpu and lspci are not installed the program hangs on macOS instead of spawning dialog
    def generate_files(self, window:QMainWindow):
        try:
            # TODO: change to generate_files.sh
            process = sp.Popen(["./test.sh"], shell=True)
            process.wait(timeout=20)
            new_widget = FileGenerated()
            window.setCentralWidget(new_widget)

        except sp.CalledProcessError as err:
            QMessageBox.critical(self, "Error", "Something went wrong while running 'generate_files.sh'. Here is the stderr:\n" + err.output)

        except FileNotFoundError as e:
            print("I couldn't find the 'generate_files.sh' script in the current directory. Please import it and try again.")

        except Exception as e:
            print("What the fuck did you do\n" + str(e))

class FileGenerated(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.label = QLabel("Everything went fine. Click the button below if you want to proceed with the data extraction.\n"
                            "You will be able to review the data after this process.")
        self.extract_data_button = QPushButton("Extract data from output files")

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.extract_data_button)
        h_box.addStretch()

        v_box = QVBoxLayout()
        v_box.addWidget(self.label)
        v_box.addSpacing(15)
        v_box.addLayout(h_box)

        self.setLayout(v_box)




def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()