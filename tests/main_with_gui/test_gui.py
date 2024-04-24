import pytest
from PyQt5 import QtCore, QtWidgets

from peracotta import CONFIG
from peracotta.gui import GUI


@pytest.fixture
def widget(qtbot):
    app = QtWidgets.QApplication.instance()
    window = GUI(app, CONFIG["TARALLO_TOKEN"])
    qtbot.addWidget(window)
    return window


@pytest.mark.gui
class TestGui:
    def test_visible(self, widget, qtbot) -> None:
        widget.show()
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

    """ def def_gpu_location(self, gpu_loc):
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
 """
