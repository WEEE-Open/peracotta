import os

import pytest
from PyQt6 import QtCore, QtTest, QtWidgets

# from main_with_gui import Welcome, FilesGenerated, GPU, DataToTarallo

gpu_loc_file = "gpu_location.txt"

test_folders = [entries for entries in os.listdir("tests/source_files/") if os.path.isdir(f"tests/source_files/{entries}")]
for fold in set(test_folders):
    if "baseboard.txt" not in os.listdir(f"tests/source_files/{fold}"):
        test_folders.remove(fold)


@pytest.fixture(params=test_folders)
def folders(request):
    return request.param


@pytest.fixture
def open_welcome(qtbot):
    def callback(window):
        widget = window(QtWidgets.QMainWindow)
        qtbot.addWidget(widget)
        widget.show()
        qtbot.wait_for_window_shown(widget)
        return widget

    return callback


@pytest.fixture
def open_filesgen(qtbot):
    def callback(window, gpu_loc: GPU):
        widget = window(Welcome, gpu_loc)
        qtbot.addWidget(widget)
        widget.show()
        qtbot.wait_for_window_shown(widget)
        # QtTest.QTest.qWait(3 * 1000)
        return widget

    return callback


def get_gpu_location(directory):
    with open(os.path.join(directory, gpu_loc_file)) as f:
        return GPU(f.read())


@pytest.mark.gui
class TestVisibleWindow:
    def test_visible_welcome(self, open_welcome, qtbot):
        widget = open_welcome(Welcome)
        assert widget.isVisible()

    def test_visible_filesgen(self, open_filesgen, qtbot):
        widget = open_filesgen(FilesGenerated, GPU.dec_gpu)
        assert widget.isVisible()


@pytest.mark.gui
class TestDataTarallo:
    def press_upload(self, widget, qtbot):
        qtbot.mouseClick(widget.btnupl, QtCore.Qt.LeftButton)
        w = widget.focusWidget()
        assert isinstance(w, QtWidgets.QPushButton)
        name = w.text()
        assert name == "Upload"

    def check_result(self):
        messagebox = QtWidgets.QApplication.activeWindow()
        text = messagebox.text()
        assert text == "Everything went fine, what do you want to do?"
        messagebox.close()

    def def_gpu_location(self, gpu_loc):
        if gpu_loc == GPU.int_mobo:
            has_dedicated_gpu = False
            gpu_in_cpu = False
        elif gpu_loc == GPU.int_cpu:
            has_dedicated_gpu = False
            gpu_in_cpu = True
        elif gpu_loc == GPU.dec_gpu:
            has_dedicated_gpu = True
            gpu_in_cpu = False
        return has_dedicated_gpu, gpu_in_cpu

    def test_no_pref(self, qtbot, folders):
        gpu_loc = get_gpu_location(os.path.join(os.getcwd(), "tests/source_files", folders))
        has_dedicated_gpu, gpu_in_cpu = self.def_gpu_location(gpu_loc)
        files_dir = os.path.join(os.getcwd(), "tests/source_files", folders)
        system_info = extract_and_collect_data_from_generated_files(files_dir, has_dedicated_gpu, gpu_in_cpu)
        widget = DataToTarallo(system_info)
        widget.show()
        QtTest.QTest.qWait(100)
        self.press_upload(widget, qtbot)
        QtTest.QTest.qWait(100)
        self.check_result()

    def test_id(self, qtbot, folders):
        gpu_loc = get_gpu_location(os.path.join(os.getcwd(), "tests/source_files", folders))
        has_dedicated_gpu, gpu_in_cpu = self.def_gpu_location(gpu_loc)
        files_dir = os.path.join(os.getcwd(), "tests/source_files", folders)
        system_info = extract_and_collect_data_from_generated_files(files_dir, has_dedicated_gpu, gpu_in_cpu)
        widget = DataToTarallo(system_info)
        widget.show()
        widget.txtid.setText(folders)
        QtTest.QTest.qWait(100)
        self.press_upload(widget, qtbot)
        QtTest.QTest.qWait(100)
        self.check_result()

    def test_overwrite(self, qtbot, folders):
        gpu_loc = get_gpu_location(os.path.join(os.getcwd(), "tests/source_files", folders))
        has_dedicated_gpu, gpu_in_cpu = self.def_gpu_location(gpu_loc)
        files_dir = os.path.join(os.getcwd(), "tests/source_files", folders)
        system_info = extract_and_collect_data_from_generated_files(files_dir, has_dedicated_gpu, gpu_in_cpu)
        widget = DataToTarallo(system_info)
        widget.show()
        widget.chbov.setChecked(True)
        QtTest.QTest.qWait(100)
        self.press_upload(widget, qtbot)
        QtTest.QTest.qWait(100)
        self.check_result()

    def test_over_id(self, qtbot, folders):
        gpu_loc = get_gpu_location(os.path.join(os.getcwd(), "tests/source_files", folders))
        has_dedicated_gpu, gpu_in_cpu = self.def_gpu_location(gpu_loc)
        files_dir = os.path.join(os.getcwd(), "tests/source_files", folders)
        system_info = extract_and_collect_data_from_generated_files(files_dir, has_dedicated_gpu, gpu_in_cpu)
        widget = DataToTarallo(system_info)
        widget.show()
        widget.chbov.setChecked(True)
        widget.txtid.setText(folders)
        QtTest.QTest.qWait(100)
        self.press_upload(widget, qtbot)
        QtTest.QTest.qWait(100)
        self.check_result()
