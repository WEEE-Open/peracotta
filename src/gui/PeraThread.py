import sys

from PyQt6 import QtCore, QtWidgets

from peracotta import commons
from peracotta.constants import PATH


class PeracottaThread(QtCore.QThread):
    updateEvent = QtCore.pyqtSignal(list, name="update")
    errorEvent = QtCore.pyqtSignal(str, str, name="error")
    startEvent = QtCore.pyqtSignal()

    def __init__(self, main_window: QtWidgets.QMainWindow):
        super().__init__()
        self.main_window = main_window

        self.gpu_location = None
        self.owner = ""
        self.files_path = PATH["TMP_FILES"]
        self.raw_files_path = ""
        self.generate_files = False
        self.filters = set()
        self.use_sudo = False
        self.sudo_passwd = None
        # self.set_default_values()

    def begin(self, generate_files: bool = True, raw_files_path: str = ""):
        self.generate_files = generate_files
        self.raw_files_path = raw_files_path
        self.start()

    def run(self) -> None:
        self.startEvent.emit()
        result = []
        try:
            if sys.platform == "win32":
                from scripts.get_windows_specs import generate_win_files

                generate_win_files()
                result = self.process_win_files()
            else:
                if self.generate_files:
                    # message = peracommon.check_required_files(self.files_path, is_gui=True)
                    # if message != "":
                    #     QtWidgets.QMessageBox.critical(self.main_window, "Error", message)
                    try:
                        self.files_path = commons.generate_files(self.files_path, self.use_sudo, self.sudo_passwd)
                    except commons.SudoError as error:
                        self.errorEvent.emit("Sudo error", str(error))
                        return
                    except commons.GenerateFilesError as error:
                        self.errorEvent.emit("Generate files error", str(error))
                        return
                    if self.files_path is None:
                        QtWidgets.QMessageBox.warning(self.main_window, "Critical error", "Failed to generate files")
                        return
                result = commons.call_parsers(
                    self.files_path,
                    set(self.filters),
                    self.gpu_location,
                    False,
                )
            if self.owner != "":
                result = commons.add_owner(result, self.owner)
            result = commons.split_products(result)
        finally:
            self.set_default_values()
        self.updateEvent.emit(result)

    def set_default_values(self):
        self.gpu_location = None
        self.owner = ""
        self.files_path = PATH["TMP_FILES"]
        self.raw_files_path = ""
        self.generate_files = False
        self.filters = set()
        self.use_sudo = False
        self.sudo_passwd = None

    def process_win_files(self):
        import parsers.windows_parser as win

        result = win.parse_win_cpu_specs(self.files_path)
        result = result + win.parse_win_chassis_specs(self.files_path)
        result = result + win.parse_win_ram_specs(self.files_path)
        result = result + win.parse_win_motherboard_specs(self.files_path)
        return result
