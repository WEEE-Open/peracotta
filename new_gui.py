from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QAbstractTableModel
from collections import defaultdict
from os.path import expanduser
import sys
import traceback
import json
import prettyprinter

VERSION = '2.0'

TARALLO_TOKEN = 'lollone'

URL = {
    "website": "https://weeeopen.polito.it",
    "source_code": "https://github.com/WEEE-Open/peracotta",
}

PATH = {
    "UI": "interface.ui",
    "JSON": "copy_this_to_tarallo.json",
    "FEATURES": "features.json",
}

ICON = {
    "case": "assets/case.png",
    "ram": "assets/ram.png",
    "cpu": "assets/cpu.png",
    "gpu": "assets/gpu.png",
    "odd": "assets/odd.png",
    "hard disk": "assets/hard disk.png",
    "motherboard": "assets/motherboard.png"
}

class Ui(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication) -> None:
        super(Ui, self).__init__()
        uic.loadUi(PATH["UI"], self)
        self.app = app
        self.peracotta = Peracotta()
        self.peracotta.updateEvent.connect(self.peracotta_results)
        self.data = None
        self.selectors = dict()
        self.useful_default_features = dict()

        # Output toolbox
        self.toolBox = self.findChild(QtWidgets.QToolBox, "toolBox")

        # Gpu location layout
        self.gpuGroupBox = self.findChild(QtWidgets.QGroupBox, "gpuGroupBox")

        # Selectors area
        self.selectorsWidget = self.findChild(QtWidgets.QWidget, "selectorsWidget")

        # Owner line edit
        self.ownerLineEdit = self.findChild(QtWidgets.QLineEdit, "ownerLineEdit")

        # Generate data button
        self.generateBtn = self.findChild(QtWidgets.QPushButton, "generateBtn")
        self.generateBtn.clicked.connect(self.generate)

        # Reset selectors button
        self.resetBtn = self.findChild(QtWidgets.QPushButton, "resetBtn")
        self.resetBtn.clicked.connect(self.reset_setup_group)

        # Save JSON button
        self.saveJsonBtn = self.findChild(QtWidgets.QPushButton, "saveJsonBtn")
        self.saveJsonBtn.clicked.connect(self.save_json)

        # Upload to tarallo button
        self.uploadBtn = self.findChild(QtWidgets.QPushButton, "uploadBtn")
        self.uploadBtn.clicked.connect(self.upload_to_tarallo)

        # Menus
        self.actionOpen = self.findChild(QtWidgets.QAction, "actionOpen")
        self.actionOpen.triggered.connect(self.open_json)
        self.actionOpenJson = self.findChild(QtWidgets.QAction, "actionOpenJson")
        self.actionOpenJson.triggered.connect(self.show_json)
        self.actionExit = self.findChild(QtWidgets.QAction, "actionExit")
        self.actionExit.triggered.connect(self.close)
        self.actionAboutUs = self.findChild(QtWidgets.QAction, "actionAboutUs")
        self.actionAboutUs.triggered.connect(self.open_website)
        self.actionSourceCode = self.findChild(QtWidgets.QAction, "actionSourceCode")
        self.actionSourceCode.triggered.connect(self.open_source_code)
        self.actionVersion = self.findChild(QtWidgets.QAction, "actionVersion")
        self.actionVersion.triggered.connect(self.show_version)

        self.show()
        self.setup()

    def setup(self):
        try:
            self.reset_toolbox()
            with open(PATH["FEATURES"], "r") as file:
                default_feature_names = {}
                default_feature_types = {}
                default_feature_values = {}
                default_features = json.load(file)
                for group in default_features["features"]:
                    for feature in default_features["features"][group]:
                        name = feature["name"]
                        default_feature_names[name] = feature["printableName"]
                        default_feature_types[name] = feature["type"]
                        if "values" in feature:
                            default_feature_values[name] = feature["values"]
                self.useful_default_features = {
                    "names": default_feature_names,
                    "types": default_feature_types,
                    "values": default_feature_values,
                }

        except FileNotFoundError:
            print("DOWNLOAD THE THING FROM TARALLO NOW!")
            useful_default_features = {}

        if self.data is None:
            return

    # utilities
    def reset_toolbox(self):
        print(self.toolBox.count())
        for idx in range(0, self.toolBox.count() + 1):
            self.toolBox.layout().removeWidget(
                self.toolBox.findChild(QtWidgets.QTableView)
            )
            self.toolBox.removeItem(idx)

    def open_url(self, url_type: str):
        url = QtCore.QUrl(url_type)
        if not QtGui.QDesktopServices.openUrl(url):
            QtWidgets.QMessageBox.warning(self, 'Cannot Open Url', f'Could not open url {url_type}')

    @staticmethod
    def print_type_cool(the_type: str) -> str:
        if the_type in ("cpu", "ram", "hdd", "odd"):
            return the_type.upper()
        else:
            return the_type.title()

    # buttons functions
    def reset_setup_group(self):
        # reset gpu location
        for radioBtn in self.gpuGroupBox.findChildren(QtWidgets.QRadioButton):
            radioBtn.setAutoExclusive(False)
            radioBtn.setChecked(False)
            radioBtn.setAutoExclusive(True)

        # reset checkboxes
        defaults = ['case', 'motherboard', 'cpu', 'gpu', 'ram', 'hard disk', 'odd']
        for checkbox in self.selectorsWidget.findChildren(QtWidgets.QCheckBox):
            if checkbox.text().lower() in defaults:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

        # reset owner
        self.ownerLineEdit.clear()

    def generate(self):
        self.peracotta.start()
        # REMOVE AFTER TESTS
        self.open_json()

        self.reset_toolbox()

        for checkbox in self.selectorsWidget.children():
            if isinstance(checkbox, QtWidgets.QVBoxLayout):
                continue
            self.selectors.update({checkbox.text().lower(): checkbox.isChecked()})

        encountered_types_count = defaultdict(lambda: 0)
        encountered_types_current_count = defaultdict(lambda: 0)
        for entry in self.data:
            the_type = entry["features"]["type"]
            encountered_types_count[the_type] += 1

        for idx, entry in enumerate(self.data):
            the_type = entry["features"]["type"]
            if not self.selectors[the_type]:
                continue
            counter = ""
            if encountered_types_count[the_type] >= 2:
                encountered_types_current_count[the_type] += 1
                counter = f" #{encountered_types_current_count[the_type]}"
            self.toolBox.addItem(
                ToolBoxWidget(entry["features"], self.useful_default_features),
                f"{self.print_type_cool(the_type)}{counter}",
            )
            icon = QtGui.QIcon(ICON[the_type])
            self.toolBox.setItemIcon(idx, icon)

    def save_json(self):
        if self.data is None:
            QtWidgets.QMessageBox.warning(self, "Warning", "There is nothing to be saved")
            return
        the_dir = QtWidgets.QFileDialog.getSaveFileName(self,
                                                        "Save Peracotta JSON",
                                                        f"{expanduser('~')}",
                                                        "JSON (*.json);;Text file (*.txt);;All Files (*)")
        if the_dir[0] == '':
            return
        with open(the_dir[0], "w") as file:
            file.write(f"{self.data}")
            file.flush()
            file.close()

    def upload_to_tarallo(self):
        # TODO: make all the things
        print(f"{TARALLO_TOKEN} - uploaded to tarallo ahahah xd")

    # menu actions
    def open_json(self):
        # the_dir = QtWidgets.QFileDialog.getOpenFileName(self, "title",
        #                                             f"{expanduser('~')}",
        #                                             f"JSON (*.json);;All Files (*)",
        #                                             )
        # if the_dir[0] == '':
        #     self.data = None
        #     return
        # with open(the_dir[0], "r") as file:
        #     self.data = json.load(file)
        with open(PATH["JSON"], "r") as file:
            self.data = json.load(file)
        # self.generate()

    def show_json(self):
        if self.data is None:
            return
        JsonWidget(self.data)

    def open_website(self):
        self.open_url(URL["website"])

    def open_source_code(self):
        self.open_url(URL["source_code"])

    def show_version(self):
        QtWidgets.QMessageBox.about(self, "Version", f"Peracotta v{VERSION}")

    # multithread
    def peracotta_results(self, data):
        # TODO: analyze data from peracotta thread
        print("peracotta terminated")

    # close event
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.peracotta.isRunning():
            self.peracotta.terminate()


class ToolBoxWidget(QtWidgets.QTableView):
    def __init__(self, data: dict, default_features: dict):
        super().__init__()
        self.verticalHeader().hide()
        self.setModel(CustomTableModel(data, default_features))
        self.horizontalHeader().setStretchLastSection(True)
        self.resizeColumnsToContents()
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data: dict, default_features: dict):
        super().__init__()
        self.features = data
        self.feature_keys = list(self.features.keys())
        self.default_features = default_features

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.features)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    # noinspection PyMethodOverriding
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return "Feature"
            else:
                return "Value"
        return None

    def flags(self, index):
        if index.column() == 1:
            return (
                QtCore.Qt.ItemIsEditable
                | QtCore.Qt.ItemIsEnabled
                | QtCore.Qt.ItemIsSelectable
            )
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()
        if row < 0 or row >= len(self.feature_keys):
            return None

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            column = index.column()
            name = self.feature_keys[row]
            if column == 0:
                return self.default_features["names"].get(name, name)
            elif column == 1:
                feature_type = self._get_feature_type(name)
                value = self.features[name]
                if feature_type == "e":
                    return self.default_features["values"][name].get(value, value)
                elif feature_type in ("d", "i"):
                    return prettyprinter.print_feature(name, value, feature_type)
                else:
                    return value
        elif role == QtCore.Qt.TextAlignmentRole:
            column = index.column()
            if column == 0:
                return QtCore.Qt.AlignLeft + QtCore.Qt.AlignVCenter
            elif column == 1:
                return QtCore.Qt.AlignRight + QtCore.Qt.AlignVCenter

        return None

    # noinspection PyMethodOverriding
    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            if col != 1:
                return False
            if row < 0 or row >= len(self.feature_keys):
                return False

            name = self.feature_keys[row]
            feature_type = self._get_feature_type(name)
            if isinstance(value, str):
                value = value.strip()

            if feature_type == "e":
                value = str(value).lower()
                if value not in self.default_features["values"][name]:
                    return False
            elif feature_type == "d":
                value = self._printable_to_value(name, value)
                value = float(value)
                if value <= 0:
                    return False
            elif feature_type == "i":
                value = self._printable_to_value(name, value)
                value = int(round(value))
                if value <= 0:
                    return False
            else:
                if len(value) <= 0:
                    return False
            self.features[name] = value
            return True
        return False

    @staticmethod
    def _printable_to_value(name, value):
        # noinspection PyBroadException
        try:
            value = prettyprinter.printable_to_value(
                prettyprinter.name_to_unit(name), value
            )
        except BaseException:
            value = 0
        return value

    def _get_feature_type(self, name):
        feature_type = self.default_features["types"].get(name, "s")
        return feature_type


class JsonWidget(QtWidgets.QDialog):
    def __init__(self, data):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        text_edit = QtWidgets.QPlainTextEdit()
        text_edit.setWordWrapMode(QtGui.QTextOption.NoWrap)
        text_edit.setPlainText(f"{json.dumps(data, indent=2)}")
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        self.setLayout(layout)
        self.exec_()


class Peracotta(QtCore.QThread):
    updateEvent = QtCore.pyqtSignal(str, name="update")

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        self.updateEvent.emit("asd")


def main():
    # noinspection PyBroadException
    try:
        app = QtWidgets.QApplication(sys.argv)
        # This is EXTREMELY IMPORTANT, DON'T TACH [sic], DO NOT REMOVE IT EVER
        # noinspection PyUnusedLocal
        window = Ui(app)
        app.exec_()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")

    except BaseException:
        print(traceback.print_exc(file=sys.stdout))


if __name__ == "__main__":
    main()
