import json
import os
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict

import requests
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from .. import commons
from ..config import CONF_DIR, CONFIG
from ..constants import ICON, PATH, URL, VERSION
from ..peralog import logdir, logger
from ..tarallo import TaralloUploadDialog, Uploader, tarallo_success_dialog
from .exceptions import MissingFeaturesError
from .PeraThread import PeracottaThread
from .Toolbox import ToolBoxWidget
from .widgets import ErrorDialog, JsonWidget

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
    ) -> None:
        logger.info(f"Peracotta v. {VERSION}")
        logger.info(f"Python v. {sys.version.split()[0]}")
        logger.info("Starting GUI")
        logger.info(f"Logs directory: {logdir}")
        logger.info("Configuration:")
        for k, v in CONFIG.items():
            logger.info(f"{k} = {v}")
        logger.info("")

        super(GUI, self).__init__()
        uic.loadUi(PATH["UI"], self)
        self.app = app
        self.uploader = None
        self.taralloDialog = None
        self.data = list(dict())
        self.features = dict()
        self.encountered_types_count = defaultdict(lambda: 0)
        self.active_theme = str()

        self.setWindowIcon(QtGui.QIcon(PATH["ICON"]))

        # shortcuts
        self.refreshThemeShortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.refreshThemeShortcut.activated.connect(self.refresh_theme)

        # Output toolbox
        self.outputScrollArea = self.findChild(QtWidgets.QScrollArea, "outputScrollArea")
        self.itemToolBox = None

        # App settings
        self.settings: QtCore.QSettings = QtCore.QSettings("WEEE Open", "PERACOTTA")

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
        self.actionOpen = self.findChild(QtWidgets.QAction, "actionOpen")
        self.actionOpen.triggered.connect(self.open_json)
        self.actionOpenLastJson = self.findChild(QtWidgets.QAction, "actionOpenLastJson")
        self.actionOpenLastJson.triggered.connect(self.open_latest_json)
        self.actionOpenJson = self.findChild(QtWidgets.QAction, "actionOpenJson")
        self.actionOpenJson.triggered.connect(self.show_json)
        self.actionOpenLogsDir = self.findChild(QtWidgets.QAction, "actionOpenLogsDir")
        self.actionOpenLogsDir.triggered.connect(self.open_logs_dir)
        self.actionLoadRawFiles = self.findChild(QtWidgets.QAction, "actionLoadRawFiles")
        self.actionLoadRawFiles.triggered.connect(self._load_raw_files)
        self.actionExit = self.findChild(QtWidgets.QAction, "actionExit")
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
        self.actionAboutUs = self.findChild(QtWidgets.QAction, "actionAboutUs")
        self.actionAboutUs.triggered.connect(self.open_website)
        self.actionSourceCode = self.findChild(QtWidgets.QAction, "actionSourceCode")
        self.actionSourceCode.triggered.connect(self.open_source_code)
        self.actionVersion = self.findChild(QtWidgets.QAction, "actionVersion")
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
        self.set_theme(self.settings.value("last_theme", "default"))
        self.load_features_file(CONFIG["TARALLO_FEATURES_AUTO_DOWNLOAD"])

        # Set item types available in the add item combo box
        for type_key in self.features["values"]["type"]:
            type_value = self.features["values"]["type"][type_key]
            self.addItemComboBox.addItem(type_value)
            if type_key in ICON:
                icon = QtGui.QIcon(ICON[type_key])
                self.addItemComboBox.setItemIcon(self.addItemComboBox.count() - 1, icon)

        # Set up the item toolbox
        self.itemToolBox = ToolBoxWidget(self.data, self.features, self.encountered_types_count)
        self.outputScrollArea.setWidget(self.itemToolBox)

        self.reset_toolbox()

        # Set the selectors widget
        layout = self.selectorsWidget.layout()
        niy = commons.ParserComponents.not_implemented_yet()
        for item in commons.ParserComponents:
            checkbox = QtWidgets.QCheckBox(item.value)
            if item in niy:
                checkbox.setEnabled(False)
            layout.addWidget(checkbox)
        self.reset_setup_group()

    @staticmethod
    def backup_features_json():
        shutil.copy2(PATH["FEATURES"], PATH["FEATURES"] + ".bak")

    @staticmethod
    def restore_features_json():
        shutil.move(PATH["FEATURES"] + ".bak", PATH["FEATURES"])

    def load_features_file(self, auto_update: bool):
        self.features = {}
        has_file = False

        try:
            mtime = os.path.getmtime(PATH["FEATURES"])
            self.backup_features_json()
            has_file = True
        except FileNotFoundError:
            mtime = 0

        if auto_update and time.time() - mtime > 60 * 60 * 12:
            try:
                response = requests.get(f"{CONFIG['TARALLO_URL']}/features.json", headers={"User-Agent": "peracotta", "Accept": "application/json"})
                with open(CONF_DIR.joinpath("features.json"), "w") as fs:
                    json.dump(response.json(), fs)

                has_file = True
            except requests.exceptions.ConnectionError as e:
                logger.exception("Couldn't connect to TARALLO")
                QtWidgets.QMessageBox.warning(None, "Error", f"Couldn't connect to TARALLO to update features.json")
            except Exception as e:
                logger.exception(e)
            finally:
                if not has_file:
                    try:
                        self.restore_features_json()
                        has_file = True
                    except FileNotFoundError as e:
                        pass

        if has_file:
            self.parse_features_file()
        else:
            raise MissingFeaturesError("features.json file not present")

    def parse_features_file(self):
        with open(PATH["FEATURES"], "r") as file:
            feature_names = {}
            feature_types = {}
            feature_values = {}
            features = json.load(file)
            for group in features["features"]:
                for feature in features["features"][group]:
                    name = feature["name"]
                    feature_names[name] = feature["printableName"]
                    feature_types[name] = feature["type"]
                    if "values" in feature:
                        feature_values[name] = feature["values"]
            self.features = {
                "names": feature_names,
                "types": feature_types,
                "values": feature_values,
            }

    # gui utilities

    def reset_toolbox(self):
        for idx in range(self.itemToolBox.count()):
            self.itemToolBox.removeItem(0)

    def open_url(self, url_type: str):
        url = QtCore.QUrl(url_type)
        if not QtGui.QDesktopServices.openUrl(url):
            QtWidgets.QMessageBox.warning(self, "Cannot Open Url", f"Could not open url {url_type}")

    def set_theme(self, theme: str = "default"):
        logger.debug(f"Setting theme {theme}")
        with open(f"{PATH['THEMES']}{theme}.css", "r") as file:
            self.app.setStyleSheet(file.read())
        self.settings.setValue("last_theme", theme)
        self.active_theme = theme
        logger.debug(f"Done setting theme")

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
        self.uploader = Uploader(commons.make_tree(self.data), CONFIG["TARALLO_URL"], CONFIG["TARALLO_TOKEN"], bulk_id, checkbox)
        self.uploader.successEvent.connect(self.tarallo_success)
        self.uploader.failureEvent.connect(self.tarallo_failure)
        self.uploader.start()

    def tarallo_success(self, code: str):
        self.uploader = None
        url = f"{CONFIG['TARALLO_URL']}/bulk/import#{urllib.parse.quote(code)}"
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
        logger.debug(f"Saving json from data:\n{json.dumps(self.data, indent=2)}")
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

    def open_logs_dir(self):
        if sys.platform == "win32":
            os.startfile(logdir)
        elif sys.platform == "darwin":
            subprocess.call(["open", logdir])
        else:
            subprocess.call(["xdg-open", logdir])

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
