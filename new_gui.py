from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QAbstractTableModel
import sys, traceback
import json
from collections import defaultdict
from os.path import expanduser
import prettyprinter

PATH = {"UI": "interface.ui",
        "JSON": "copy_this_to_tarallo.json",
        "FEATURES": "features.json",
        }


class Ui(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication) -> None:
        super(Ui, self).__init__()
        uic.loadUi(PATH["UI"], self)
        self.app = app
        self.data = None
        self.selectors = dict()
        self.useful_default_features = dict()

        # Output toolbox
        self.toolBox = self.findChild(QtWidgets.QToolBox, 'toolBox')

        # Selectors area
        self.selectorsWidget = self.findChild(QtWidgets.QWidget, 'selectorsWidget')

        # Generate data button
        self.generateBtn = self.findChild(QtWidgets.QPushButton, 'generateBtn')
        self.generateBtn.clicked.connect(self.generate)

        # Reset selectors button
        self.resetBtn = self.findChild(QtWidgets.QPushButton, 'resetBtn')
        self.resetBtn.clicked.connect(self.reset_toolbox)

        # Menus
        self.actionOpen = self.findChild(QtWidgets.QAction, 'actionOpen')
        self.actionOpen.triggered.connect(self.open_json)
        self.actionOpenJson = self.findChild(QtWidgets.QAction, 'actionOpenJson')
        self.actionOpenJson.triggered.connect(self.show_json)
        self.show()
        self.setup()

    @staticmethod
    def print_type_cool(the_type: str) -> str:
        if the_type in ("cpu", "ram", "hdd", "odd"):
            return the_type.upper()
        else:
            return the_type.title()

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

    def reset_toolbox(self):
        print(self.toolBox.count())
        for idx in range(0, self.toolBox.count()+1):
            self.toolBox.layout().removeWidget(self.toolBox.findChild(QtWidgets.QTableView))
            self.toolBox.removeItem(idx)

    def generate(self):
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

        for entry in self.data:
            the_type = entry["features"]["type"]
            if not self.selectors[the_type]:
                continue
            counter = ""
            if encountered_types_count[the_type] >= 2:
                encountered_types_current_count[the_type] += 1
                counter = f" #{encountered_types_current_count[the_type]}"
            self.toolBox.addItem(ToolBoxWidget(entry["features"], self.useful_default_features),
                                 f"{self.print_type_cool(the_type)}{counter}")

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
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()
        if row < 0 or row >= len(self.feature_keys):
            return None

        if role == QtCore.Qt.DisplayRole:
            column = index.column()
            name = self.feature_keys[row]
            if column == 0:
                return self.default_features["names"].get(name, name)
            elif column == 1:
                feature_type = self.default_features["types"].get(name, "s")
                value = self.features[name]
                if feature_type == "e":
                    return self.default_features["values"][name].get(value, value)
                elif feature_type in ("d", "i"):
                    return prettyprinter.print_feature(name, value)
                else:
                    return value
        elif role == QtCore.Qt.EditRole:
            column = index.column()
            name = self.feature_keys[row]
            if column == 1:
                return self.features[name]
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

            # TODO: allow deleting a feature?
            if isinstance(value, str):
                if len(value) <= 0:
                    return False
            if isinstance(value, int) or isinstance(value, float):
                if value <= 0:
                    return False

            name = self.feature_keys[row]
            feature_type = self.default_features["types"].get(name, "s")
            if feature_type == "e":
                if value not in self.default_features["values"][name]:
                    return False
            elif feature_type == "d":
                value = float(value)
            elif feature_type == "i":
                value = int(value)
            self.features[name] = value
            return True
        return False


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


def main():
    # noinspection PyBroadException
    try:
        app = QtWidgets.QApplication(sys.argv)
        # This is EXTREMEL
        # noinspection PyUnusedLocal
        window = Ui(app)
        app.exec_()

    except KeyboardInterrupt:
        print("KeyboardInterrupt")

    except BaseException:
        print(traceback.print_exc(file=sys.stdout))


if __name__ == "__main__":
    main()