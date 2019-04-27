import sys, os, subprocess
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QLabel, QWidget, QDialogButtonBox


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        welcome_widget = Welcome()
        self.setCentralWidget(welcome_widget)
        self.setWindowTitle("P.E.R.A.C.O.T.T.A.")

        self.show()

    def next_clicked(self):
        pass


class Welcome(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.welcome_message = QLabel("Welcome to P.E.R.A.C.O.T.T.A.")
        self.intro_message = QLabel(
            "(Progetto Esteso Raccolta Automatica Configurazioni hardware Organizzate Tramite Tarallo Autonomamente)\n"
            "When you're ready to generate the files required to gather info about this system, click the 'Generate files' button below.")
        # TODO: set font size (bigger for welcome_message)

        self.generate_files_button = QPushButton("Generate Files")
        self.generate_files_button.clicked.connect(self.generate_files)

        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.generate_files_button)

        v_box = QVBoxLayout()
        v_box.addWidget(self.welcome_message)
        v_box.addWidget(self.intro_message)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

    # TODO: fix when dmidecode, lscpu and lspci are not installed the program hangs on macOS instead of spawning dialog
    def generate_files(self):
        try:
            # process = subprocess.Popen(["./generate_files.sh"])
            # process.wait()
            output = subprocess.check_output("./generate_files.sh")
            next_button = QPushButton("Next")
            self.dialog = QDialogButtonBox("Everything went fine.")
            next_button.clicked.connect(self.dialog.close())
            # next_button.clicked.connect() # change main window
            self.dialog.addButton(next_button)
            self.dialog.show()
        except subprocess.CalledProcessError as err:
            # stdout, stderr = process.communicate()

            close_button = QPushButton("Close")
            self.dialog = QDialogButtonBox("Something went wrong while running 'generate_files.sh'. Here is the stderr:\n" + err.output)
            close_button.clicked.connect(self.dialog.close())
            self.dialog.addButton(close_button)
            self.dialog.show()

        except FileNotFoundError as e:
            print("I couldn't find the 'generate_files.sh' script in the current directory. Please import it and try again.")

def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()