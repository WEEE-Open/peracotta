import pytest
import os
from PyQt5 import QtCore, QtTest, QtWidgets
from main import extract_and_collect_data_from_generated_files
from main_with_gui import Welcome, FilesGenerated, GPU, DataToTarallo, get_gpu_location


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
        #QtTest.QTest.qWait(3 * 1000)
        return widget

    return callback


class TestVisibleWindow:
    def test_visible_welcome(self, open_welcome, qtbot):
        widget = open_welcome(Welcome)
        assert widget.isVisible()

    def test_visible_filesgen(self, open_filesgen, qtbot):
        widget = open_filesgen(FilesGenerated, GPU.dec_gpu)
        assert widget.isVisible()


class TestDataTarallo:
    def show_window(self):
        system_info = self.create_system_info()
        widget = DataToTarallo(system_info)
        widget.show()
        return widget

    def press_upload(self, widget, qtbot):
        qtbot.mouseClick(widget.btnupl, QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(1000)
        w = widget.focusWidget()
        assert isinstance(w, QtWidgets.QPushButton)
        name = w.text()
        assert name == "Upload"

    def check_result(self):
        messagebox = QtWidgets.QApplication.activeWindow()
        QtTest.QTest.qWait(1000)
        text = messagebox.text()
        assert text == "Everything went fine, what do you want to do?"
        messagebox.close()

    def create_system_info(self):
        gpu_loc = get_gpu_location(os.path.join(os.getcwd(), "tests/asdpc"))
        if gpu_loc == GPU.int_mobo:
            has_dedicated_gpu = False
            gpu_in_cpu = False
        elif gpu_loc == GPU.int_cpu:
            has_dedicated_gpu = False
            gpu_in_cpu = True
        elif gpu_loc == GPU.dec_gpu:
            has_dedicated_gpu = True
            gpu_in_cpu = False
        files_dir = os.path.join(os.getcwd(), "tests/asdpc")
        return extract_and_collect_data_from_generated_files(
            files_dir, has_dedicated_gpu, gpu_in_cpu
        )

    def test_no_pref(self,qtbot):
        widget = self.show_window()
        QtTest.QTest.qWait(1000)
        self.press_upload(widget, qtbot)
        self.check_result()

    def test_id(self, qtbot):
        widget = self.show_window()
        widget.txtid.setText("asdone3")#nome in base al pc
        QtTest.QTest.qWait(000)
        self.press_upload(widget, qtbot)
        self.check_result()

    def test_overwrite(self, qtbot):
        widget = self.show_window()
        widget.chbov.setChecked(True)
        QtTest.QTest.qWait(1000)
        self.press_upload(widget, qtbot)
        self.check_result()


    def test_over_id(self, qtbot):
        widget = self.show_window()
        widget.chbov.setChecked(True)
        widget.txtid.setText("asdone")  # nome in base al pc
        QtTest.QTest.qWait(1000)
        self.press_upload(widget, qtbot)
        self.check_result()

