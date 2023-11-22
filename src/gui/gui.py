import json
import os
import shutil
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from urllib.error import URLError

from peracotta.commons import ParserComponents, env_to_bool, make_tree
from peracotta.constants import ICON, PATH, VERSION, URL
from .PeraThread import PeracottaThread
from peracotta.tarallo import TaralloUploadDialog, Uploader, tarallo_success_dialog
from .Toolbox import ToolBoxWidget
from PyQt6 import QtCore, QtGui, QtWidgets, uic

from peracotta import commons

DEFAULT_PROGRESS_BAR_STYLE = (
    "QStatusBar::item {"
    "min-height: 12px;"
    "max-height: 12px;"
    "}"
    "QProgressBar {"
    "min-height: 14px;"
    "max-height: 14px;"
    "}"
    "QProgressBar::chunk {"
    "background-color: #00963A;"
    "width: 50px;"
    "}"
)


class GUI(QtWidgets.QMainWindow):
    def __init__(
        self,
        app: QtWidgets.QApplication,
        tarallo_url: str,
        tarallo_token: str,
    ) -> None:
        super(GUI, self).__init__()
        uic.loadUi(PATH["UI"], self)
        self.app = app
        self.uploader = None
        self.taralloDialog = None
        self.data = list(dict())
        self.tarallo_url = tarallo_url
        self.tarallo_token = tarallo_token
        self.useful_default_features = dict()
        self.encountered_types_count = defaultdict(lambda: 0)
        self.active_theme = str()

        self.setWindowIcon(QtGui.QIcon(PATH["ICON"]))

        # shortcuts
        self.refreshThemeShortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.refreshThemeShortcut.activated.connect(self.refresh_theme)

        # Output toolbox
        self.outputScrollArea = self.findChild(QtWidgets.QScrollArea, "outputScrollArea")
        self.itemToolBox = None

        # App settings
        self.settings = QtCore.QSettings("WEEE Open", "PERACOTTA")

        # Gpu location layout
        self.gpuGroupBox = self.findChild(QtWidgets.QGroupBox, "gpuGroupBox")

        # Radio buttons
        self.discreteRadioBtn = self.findChild(QtWidgets.QRadioButton, "discreteRadioBtn")
        self.intCpuRadioBtn = self.findChild(QtWidgets.QRadioButton, "intCpuRadioBtn")
        self.intMoboRadioBtn = self.findChild(QtWidgets.QRadioButton, "intMoboRadioBtn")
        self.bothGpuRadioBtn = self.findChild(QtWidgets.QRadioButton, "bothGpuRadioBtn")

        # Selectors area
        self.selectorsWidget = self.findChild(QtWidgets.QWidget, "selectorsWidget")
        self.selectorsScrollArea = self.findChild(QtWidgets.QScrollArea, "selectorsScrollArea")

        self.addItemComboBox = self.findChild(QtWidgets.QComboBox, "addItemComboBox")
        self.addItemComboBox.addItem("Select Type --")
        self.addItemComboBox.currentTextChanged.connect(self.add_toolbox_item)
        self.addItemComboBox.wheelEvent = lambda stop_wheel_event: None

        # 'select/deselect all' buttons
        self.selectAllBtn = self.findChild(QtWidgets.QPushButton, "selectBtn")
        self.selectAllBtn.clicked.connect(self.select_all_checkboxes)
        self.deselectAllBtn = self.findChild(QtWidgets.QPushButton, "deselectBtn")
        self.deselectAllBtn.clicked.connect(self.deselect_all_checkboxes)

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
        self.uploadBtn.clicked.connect(self.tarallo_dialog)

        # File actions
        self.actionOpen = self.findChild(QtGui.QAction, "actionOpen")
        self.actionOpen.triggered.connect(self.open_json)
        self.actionOpenLastJson = self.findChild(QtGui.QAction, "actionOpenLastJson")
        self.actionOpenLastJson.triggered.connect(self.open_latest_json)
        self.actionOpenJson = self.findChild(QtGui.QAction, "actionOpenJson")
        self.actionOpenJson.triggered.connect(self.show_json)
        self.actionLoadRawFiles = self.findChild(QtGui.QAction, "actionLoadRawFiles")
        self.actionLoadRawFiles.triggered.connect(self._load_raw_files)
        self.actionExit = self.findChild(QtGui.QAction, "actionExit")
        self.actionExit.triggered.connect(self.close)

        # Options actions
        self.menuTheme = self.findChild(QtWidgets.QMenu, "menuTheme")
        action = list()
        action.append(self.menuTheme.addAction("Default"))
        action[-1].triggered.connect(lambda: self.set_theme("default"))
        for theme_file in os.listdir(PATH["THEMES"]):
            theme = theme_file.rstrip(".css")
            action.append(self.menuTheme.addAction(theme))
            action[-1].triggered.connect((lambda t: lambda: self.set_theme(t))(theme))

        # Help actions
        self.actionAboutUs = self.findChild(QtGui.QAction, "actionAboutUs")
        self.actionAboutUs.triggered.connect(self.open_website)
        self.actionSourceCode = self.findChild(QtGui.QAction, "actionSourceCode")
        self.actionSourceCode.triggered.connect(self.open_source_code)
        self.actionVersion = self.findChild(QtGui.QAction, "actionVersion")
        self.actionVersion.triggered.connect(self.show_version)

        # Status bar widgets
        self.progressBar = QtWidgets.QProgressBar()
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.hide()
        # self.statusBar().setStyleSheet(DEFAULT_PROGRESS_BAR_STYLE)

        # Setup peracotta QThread
        self.perathread = PeracottaThread(self)
        self.perathread.updateEvent.connect(self.peracotta_results)
        self.perathread.startEvent.connect(self.show_busy_progress_bar)
        self.perathread.errorEvent.connect(self.peracotta_error)

        self.errorDialog = None

        self.show()
        self.setup()

    def setup(self):
        self.get_settings()
        self.set_theme(self.active_theme)
        self.download_features()

        # Set item types available in the add item combo box
        for type_key in self.useful_default_features["values"]["type"]:
            type_value = self.useful_default_features["values"]["type"][type_key]
            self.addItemComboBox.addItem(type_value)
            if type_key in ICON:
                icon = QtGui.QIcon(ICON[type_key])
                self.addItemComboBox.setItemIcon(self.addItemComboBox.count() - 1, icon)

        # Set up the item toolbox
        self.itemToolBox = ToolBoxWidget(self.data, self.useful_default_features, self.encountered_types_count)
        self.outputScrollArea.setWidget(self.itemToolBox)

        self.reset_toolbox()

        # Set the selectors widget
        layout = self.selectorsWidget.layout()
        niy = ParserComponents.not_implemented_yet()
        for item in ParserComponents:
            checkbox = QtWidgets.QCheckBox(item.value)
            if item in niy:
                checkbox.setEnabled(False)
            layout.addWidget(checkbox)
        self.reset_setup_group()

    def download_features(self):
        # self.useful_default_features must be set correctly, otherwise the GUI will fail to load
        try:
            tarallo_auto_download = env_to_bool(os.environ.get("TARALLO_FEATURES_AUTO_DOWNLOAD", "1"))
            self.load_features_file(tarallo_auto_download)
        except Exception as e:
            title = "Cannot download features"
            message = f"Failed to download features from TARALLO: {str(e)}"
            if self.useful_default_features == {}:
                QtWidgets.QMessageBox.critical(
                    self,
                    title,
                    message + "\n\nPeracotta will now terminate.\nIf the problem persists, you can try peracruda instead.",
                )
                exit(1)
            else:
                QtWidgets.QMessageBox.warning(self, title, message)

    def get_settings(self):
        self.active_theme = self.settings.value("last_theme")
        if self.active_theme is None:
            self.active_theme = "default"

    @staticmethod
    def _backup_features_json() -> bool:
        here = os.path.dirname(os.path.realpath(__file__))
        try:
            shutil.copy2(
                os.path.join(here, "features.json"),
                os.path.join(here, "features.json.bak"),
            )
        except FileNotFoundError:
            return False
        return True

    @staticmethod
    def _restore_features_json() -> bool:
        here = os.path.dirname(os.path.realpath(__file__))
        try:
            shutil.move(
                os.path.join(here, "features.json.bak"),
                os.path.join(here, "features.json"),
            )
        except FileNotFoundError:
            return False
        return True

    def load_features_file(self, auto_update: bool):
        self.useful_default_features = {}
        has_file = False
        error = None

        try:
            mtime = os.path.getmtime(PATH["FEATURES"])
            has_file = True
        except FileNotFoundError:
            mtime = 0

        if auto_update and time.time() - mtime > 60 * 60 * 12:
            # TODO: etag/if-modified-since
            request = urllib.request.Request(url=f"{self.tarallo_url}/features.json")
            request.add_header("User-Agent", "peracotta")
            request.add_header("Accept", "application/json")
            self._backup_features_json()
            # noinspection PyBroadException
            try:
                with urllib.request.urlopen(request) as response:
                    with open("features.json", "wb") as out:
                        shutil.copyfileobj(response, out)
                        has_file = True
            except URLError as e:
                if hasattr(e, "reason"):
                    error = "Connection error: " + str(e.reason)
                elif hasattr(e, "code"):
                    error = "Server error: " + str(e.code)
            except Exception as e:
                error = "Some error: " + str(e)

            if error:
                has_file = self._restore_features_json()

        if has_file:
            self._parse_features_file()

        if error:
            raise Exception(error)
        if not has_file and not auto_update:
            raise Exception("features.json file not present and automatic download is disabled")

    def _parse_features_file(self):
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

    # gui utilities

    def reset_toolbox(self):
        for idx in range(self.itemToolBox.count()):
            self.itemToolBox.removeItem(0)

    def open_url(self, url_type: str):
        url = QtCore.QUrl(url_type)
        if not QtGui.QDesktopServices.openUrl(url):
            QtWidgets.QMessageBox.warning(self, "Cannot Open Url", f"Could not open url {url_type}")

    def set_theme(self, theme: str):
        if theme == "default":
            self.app.setStyleSheet("")
            self.app.setStyleSheet("QWidget {" "font-size: 10pt;" "}")
            self.active_theme = "default"
        else:
            with open(f"{PATH['THEMES']}{theme}.css", "r") as file:
                self.app.setStyleSheet(file.read())
        self.settings.setValue("last_theme", theme)
        self.active_theme = theme

    def refresh_theme(self):
        if self.active_theme == "default":
            return
        with open(f"{PATH['THEMES']}{self.active_theme}.css", "r") as file:
            self.app.setStyleSheet(file.read())

    def show_busy_progress_bar(self):
        self.progressBar.setRange(0, 0)
        self.progressBar.show()

    def select_all_checkboxes(self):
        for checkbox in self.selectorsWidget.findChildren(QtWidgets.QCheckBox):
            if checkbox.isEnabled():
                checkbox.setChecked(True)

    def deselect_all_checkboxes(self):
        for checkbox in self.selectorsWidget.findChildren(QtWidgets.QCheckBox):
            checkbox.setChecked(False)

    def get_file_directory_dialog(self):
        the_dir = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open JSON",
            f"{os.path.expanduser('~')}",
            f"JSON (*.json);;All Files (*)",
        )
        return the_dir[0]

    def get_directory_dialog(self):
        the_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Open JSON", f"{os.path.expanduser('~')}")
        return the_dir if the_dir != "" else None

    # tarallo utilities

    def upload_to_tarallo(self, checkbox: bool, bulk_id=None):
        if bulk_id == "":
            bulk_id = None
        self.uploader = Uploader(make_tree(self.data), self.tarallo_url, self.tarallo_token, bulk_id, checkbox)
        self.uploader.successEvent.connect(self.tarallo_success)
        self.uploader.failureEvent.connect(self.tarallo_failure)
        self.uploader.start()

    def tarallo_success(self, code: str):
        self.uploader = None
        url = f"{self.tarallo_url}/bulk/import#{urllib.parse.quote(code)}"
        tarallo_success_dialog(url)

    def tarallo_failure(self, case: str, bulk_id: str):
        self.uploader = None
        if case == "cannot_upload":
            QtWidgets.QMessageBox.warning(
                self,
                "Cannot upload to T.A.R.A.L.L.O.",
                "Cannot upload, try to change the bulk identifier or check the overwrite checkbox.",
            )
            self.tarallo_dialog(bulk_id)
        elif case == "cannot_reach":
            QtWidgets.QMessageBox.warning(
                self,
                "Unable to reach the T.A.R.A.L.L.O.",
                "Please connect this PC to the Internet and try again.",
            )

    # buttons functions

    def reset_setup_group(self):
        # reset gpu location
        for radioBtn in self.gpuGroupBox.findChildren(QtWidgets.QRadioButton):
            radioBtn.setAutoExclusive(False)
            radioBtn.setChecked(False)
            radioBtn.setAutoExclusive(True)

        # reset checkboxes
        defaults = set(commons.ParserComponents.all_names()) - {
            commons.ParserComponents.MONITOR.value,
            commons.ParserComponents.INPUT.value,
        }

        for checkbox in self.selectorsWidget.findChildren(QtWidgets.QCheckBox):
            checkbox: QtWidgets.QCheckBox
            if checkbox.text() in defaults and checkbox.isEnabled():
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
                checkbox.setStyleSheet("text-decoration: line-through;")

        # reset owner
        self.ownerLineEdit.clear()

    def gpu_location_from_buttons(self):
        if self.discreteRadioBtn.isChecked():
            return commons.GpuLocation.DISCRETE
        if self.intCpuRadioBtn.isChecked():
            return commons.GpuLocation.CPU
        if self.intMoboRadioBtn.isChecked():
            return commons.GpuLocation.MOTHERBOARD
        if self.bothGpuRadioBtn.isChecked():
            QtWidgets.QMessageBox.information(
                self,
                "Warning",
                "The integrated GPU cannot be detected in this configuration: disconnect the dedicated one and re-run peracotta if you want to parse it, or edit manually.",
            )
            return commons.GpuLocation.DISCRETE
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please, select one of the GPU locations to proceed.")
            return None

    def get_selected_filters(self):
        filters = set()
        for checkbox in self.selectorsWidget.findChildren(QtWidgets.QCheckBox):
            checkbox: QtWidgets.QCheckBox
            if checkbox.isChecked():
                filters.add(commons.ParserComponents(checkbox.text()))
        return filters

    def generate(self):
        if self.perathread.isRunning():
            return

        if not self.set_thread_buttons_values():
            self.perathread.set_default_values()
            return

        if sys.platform != "win32":
            use_sudo = commons.env_to_bool(os.environ.get("GENERATE_FILES_USE_SUDO", "1"))
            ask_sudo_pass = commons.env_to_bool(os.environ.get("GENERATE_FILES_ASK_SUDO_PASSWORD", "1"))

            if use_sudo and "NOPASSWD: ALL" in os.popen("sudo -l").read():
                ask_sudo_pass = False

            self.perathread.use_sudo = use_sudo

            if use_sudo and ask_sudo_pass:
                got_it = self._ask_sudo_pass()
                if not got_it:
                    return
            else:
                self.perathread.sudo_passwd = None

        self.perathread.generate_files = True
        # TODO: shouldn't the next 2 lines be reversed?
        self.perathread.begin()
        self.reset_toolbox()

    def set_thread_buttons_values(self):
        gpu_location = self.gpu_location_from_buttons()
        if gpu_location is None:
            return False
        self.perathread.gpu_location = gpu_location
        self.perathread.owner = self.ownerLineEdit.text()
        self.perathread.filters = self.get_selected_filters()
        return True

    def _ask_sudo_pass(self):
        sudo_passwd, ok = QtWidgets.QInputDialog.getText(
            self,
            "Insert sudo password",
            "Insert sudo password:",
            QtWidgets.QLineEdit.EchoMode.Password,
        )
        if ok:
            self.perathread.sudo_passwd = sudo_passwd
            return True
        else:
            self.perathread.sudo_passwd = None
            return False

    def save_json(self):
        if self.data is None:
            QtWidgets.QMessageBox.warning(self, "Warning", "There is nothing to be saved")
            return
        the_dir = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Peracotta JSON",
            f"{os.path.expanduser('~')}",
            "JSON (*.json);;Text file (*.txt);;All Files (*)",
        )
        if the_dir[0] == "":
            return
        with open(the_dir[0], "w") as file:
            file.write(f"{json.dumps(commons.make_tree(self.data), indent=2)}")

    def tarallo_dialog(self, bulk_id=str()):
        if len(self.data) == 0:
            QtWidgets.QMessageBox.warning(self, "Warning", "There is nothing to be uploaded")
            return
        if not bulk_id:
            bulk_id = ""
        taralloDialog = TaralloUploadDialog(self, bulk_id)
        taralloDialog.signal.connect(self.upload_to_tarallo)

    def add_toolbox_item(self):
        if self.addItemComboBox.currentIndex() == 0:
            return
        else:
            item_type = self.addItemComboBox.currentText().lower()
            self.itemToolBox.add_item(item_type=item_type, single_item=True)
            if self.data is None:
                self.data = []
            self.data.append({})
            self.addItemComboBox.setCurrentIndex(0)

    # menu actions

    def open_json(self, path: str = ""):
        if not path:
            path = self.get_file_directory_dialog()
        if path == "":
            self.data = None
            return
        try:
            with open(path, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError as exc:
            QtWidgets.QMessageBox.warning(self, "Error", f"File not found.\n{exc.args[1]}")

        self.data = commons.unmake_tree(self.data)
        self.settings.setValue("latest_json", path)
        self.itemToolBox.load_items(self.data)

    def open_latest_json(self):
        for key in self.settings.childKeys():
            if "latest_json" in key:
                self.open_json(self.settings.value("latest_json"))

    # the checked parameter exists for QAction::triggered
    # noinspection PyUnusedLocal

    def _load_raw_files(self, checked):
        self.load_raw_files()

    def load_raw_files(self, path: str = ""):
        if self.perathread.isRunning():
            return

        if not self.set_thread_buttons_values():
            self.perathread.set_default_values()
            return

        if path == "":
            path = self.get_directory_dialog()
        if path is None:
            self.perathread.set_default_values()
            return
        self.perathread.generate_files = False
        self.perathread.files_path = path

        # TODO: shouldn't the next 2 lines be reversed?
        self.perathread.begin()
        self.reset_toolbox()

    def show_json(self):
        if self.data is None:
            return
        JsonWidget(commons.make_tree(self.data), self.size())

    def open_website(self):
        self.open_url(URL["website"])

    def open_source_code(self):
        self.open_url(URL["source_code"])

    def show_version(self):
        QtWidgets.QMessageBox.about(self, "Version", f"Peracotta v{VERSION}")

    # multithread
    def peracotta_results(self, data: list):
        self.progressBar.setRange(0, 1)  # disable statusBar's progressBar
        self.progressBar.hide()
        if not data:
            return
        self.data = data
        self.itemToolBox.load_items(self.data)

    def peracotta_error(self, error_type: str, error: str):
        self.errorDialog = ErrorDialog(self, error_type, error)
        self.progressBar.setRange(0, 1)  # disable statusBar's progressBar
        self.progressBar.hide()

    # close event
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.perathread.isRunning():
            self.perathread.terminate()


class JsonWidget(QtWidgets.QDialog):
    def __init__(self, data: list[dict], window_size: QtCore.QSize):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        text_edit = QtWidgets.QPlainTextEdit()
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
        uic.loadUi(PATH["ERRORDIALOG"], self)
        self.setWindowTitle("Error")
        self.iconLabel = self.findChild(QtWidgets.QLabel, "iconLabel")
        self.textLabel = self.findChild(QtWidgets.QLabel, "textLabel")
        self.textLabel.setText(title)
        self.errorTextEdit = self.findChild(QtWidgets.QPlainTextEdit, "errorTextEdit")
        self.errorTextEdit.setPlainText(detailed_error)
        self.show()
