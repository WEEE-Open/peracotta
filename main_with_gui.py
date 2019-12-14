#!/usr/bin/env python3

import sys
import os
import subprocess as sp
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow, QLabel, QWidget, \
	QMessageBox, QScrollArea
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from extract_data import extract_and_collect_data_from_generated_files
from polkit import make_dotfiles


class Window(QMainWindow):
	def __init__(self):
		# noinspection PyArgumentList
		super().__init__()
		self.init_ui()

	def init_ui(self):
		welcome_widget = Welcome(self)
		self.setCentralWidget(welcome_widget)

		self.setWindowTitle("P.E.R.A.C.O.T.T.A.")
		self.setWindowIcon(QIcon(os.path.join("data", "pear_emoji.png")))

		self.show()


class Welcome(QWidget):
	def __init__(self, window: QMainWindow):
		# noinspection PyArgumentList
		super().__init__()
		self.title = QLabel("Welcome to P.E.R.A.C.O.T.T.A.")
		self.subtitle = QLabel(
			"(Progetto Esteso Raccolta Automatica Configurazioni hardware Organizzate Tramite Tarallo Autonomamente)")
		self.intro = QLabel(
			"When you're ready to generate the files required to gather info about this system, click the "
			"'Generate files' button below.")

		# noinspection PyArgumentList
		title_font = QFont("futura", pointSize=24, italic=False)
		# noinspection PyArgumentList
		subtitle_font = QFont("futura", pointSize=14, italic=True)
		self.title.setFont(title_font)
		self.subtitle.setFont(subtitle_font)

		self.generate_files_button = QPushButton("Generate Files")
		# noinspection PyUnresolvedReferences
		self.generate_files_button.clicked.connect(lambda: self.prompt_has_dedicated_gpu(window))

		h_box = QHBoxLayout()
		h_box.addStretch()
		h_box.addWidget(self.generate_files_button, alignment=Qt.AlignCenter)
		h_box.addStretch()

		v_box = QVBoxLayout()
		v_box.addWidget(self.title, alignment=Qt.AlignCenter)
		v_box.addWidget(self.subtitle, alignment=Qt.AlignCenter)
		v_box.addSpacing(30)
		v_box.addWidget(self.intro, alignment=Qt.AlignCenter)
		v_box.addSpacing(15)
		v_box.addLayout(h_box)

		self.setLayout(v_box)

	def prompt_has_dedicated_gpu(self, window: QMainWindow):
		# TODO: allow NO as an answer
		while True:
			# noinspection PyCallByClass
			answer = QMessageBox.question(self,
				"Discrete GPU",
				"Does this system have a dedicated video card?",
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if answer == QMessageBox.Yes:
				# noinspection PyCallByClass
				confirm = QMessageBox.question(self, "Confirm",
					"Do you confirm this system has a dedicated video card?",
					QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				if confirm == QMessageBox.Yes:
					self.generate_files(window, has_dedicated_gpu=True)
					break
				else:
					continue
			else:
				# noinspection PyCallByClass
				confirm = QMessageBox.question(self, "Confirm",
					"Do you confirm this system has an integrated GPU?",
					QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				if confirm == QMessageBox.Yes:
					self.generate_files(window, has_dedicated_gpu=False)
					break
				else:
					continue

	def generate_files(self, window: QMainWindow, has_dedicated_gpu: bool):
		try:
			working_directory = os.getcwd()
			if not os.path.isdir(os.path.join(working_directory, "tmp")):
				os.makedirs(os.path.join(working_directory, "tmp"))

			folder_name = "tmp"
			path_to_gen_files_sh = working_directory + "/generate_files.sh"
			make_dotfiles(path_to_generate_files_sh=path_to_gen_files_sh)
			with sp.Popen(["./generate_files.pkexec", os.path.join(working_directory, folder_name)], shell=False) as process:
				process.wait(timeout=60)
			# the line below is needed in order to not close the window!
			window.takeCentralWidget()
			new_widget = FilesGenerated(window, has_dedicated_gpu)
			window.setCentralWidget(new_widget)

		except sp.CalledProcessError as err:
			# noinspection PyCallByClass
			# noinspection PyArgumentList
			QMessageBox.critical(self, "Error",
				"Something went wrong while running 'generate_files.sh'. Here is the stderr:\n" + err.output)

		except FileNotFoundError:
			# noinspection PyCallByClass
			# noinspection PyArgumentList
			QMessageBox.warning(self, "Warning",
				"I couldn't find the 'generate_files.sh' script in the current directory. Please import it and try again.")

		except Exception as e:
			# noinspection PyCallByClass
			# noinspection PyArgumentList
			QMessageBox.critical(self, "WTF1", "Have a look at the extent of your huge fuck-up:\n" + str(e))
			print(e)


class FilesGenerated(QWidget):
	def __init__(self, window: QMainWindow, has_dedicated_gpu: bool):
		# noinspection PyArgumentList
		super().__init__()
		self.label = QLabel(
			"Everything went fine. Click the button below if you want to proceed with the data extraction.\n"
			"You will be able to review the data after this process.")
		self.extract_data_button = QPushButton("Extract data from output files")
		self.extract_data_button.clicked.connect(
			lambda: self.extract_data_from_generated_files(window, has_dedicated_gpu))

		h_box = QHBoxLayout()
		h_box.addStretch()
		h_box.addWidget(self.extract_data_button, alignment=Qt.AlignCenter)
		h_box.addStretch()

		v_box = QVBoxLayout()
		v_box.addWidget(self.label, alignment=Qt.AlignCenter)
		v_box.addSpacing(15)
		v_box.addLayout(h_box)

		self.setLayout(v_box)

	def extract_data_from_generated_files(self, window: QMainWindow, has_dedicated_gpu: bool):
		try:
			system_info, print_lspci_lines_in_dialog = extract_and_collect_data_from_generated_files('tmp',
				has_dedicated_gpu, False)  # TODO: support this
			print(system_info)
			window.takeCentralWidget()

			# new_window = ScrollableWindow()
			new_widget = VerifyExtractedDataScrollable(window, system_info)
			window.setCentralWidget(new_widget)
			# new_window.setCentralWidget(new_widget)
			# window.scroll_area = QScrollArea(window.centralWidget())
			# window.layout().addWidget(window.scroll_area)

			# window.close()

		except Exception as e:
			# noinspection PyCallByClass
			# noinspection PyArgumentList
			QMessageBox.critical(self, "WTF2", "Have a look at the extent of your huge fuck-up:\n" + str(e))
			print(e)


# class ScrollableWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.scroll_area = QScrollArea(self)
#         self.scroll_area.setWidgetResizable(True)
#         self.scroll_area_widget_contents = QWidget(self.scroll_area)
#         self.scroll_area_widget_contents.setGeometry(QRect(25, 25, 380, 247))
#         self.scroll_area.setWidget(self.scroll_area_widget_contents)
#
#         self.v_box = QVBoxLayout(self)
#         self.v_box.addWidget(self.scroll_area)
#
#         self.v_box_scroll = QVBoxLayout(self.scroll_area_widget_contents)
#
#         self.show()


class VerifyExtractedData(QWidget):
	def __init__(self, window: QMainWindow, system_info):
		# noinspection PyArgumentList
		super().__init__()
		self.init_ui(window.showMaximized(), system_info)

	def init_ui(self, window: QMainWindow, system_info):

		v_box = QVBoxLayout()
		h_buttons = QHBoxLayout()

		button_style = "background-color: #006699; padding-left:20px; padding-right:20px; padding-top:5px; padding-bottom:5px;"

		# copy to the clipboard - button
		self.clipboard_button = QPushButton("Copy to clipboard")
		self.clipboard_button.setStyleSheet(button_style)
		self.clipboard_button.clicked.connect(lambda: QApplication.clipboard().setText(' '.join(str(s) for s in system_info)))
		self.clipboard_button.clicked.connect(lambda: QMessageBox.question(self, "Done", "Copied into clipboard", QMessageBox.Ok, QMessageBox.Ok))
		# go to the website - button
		self.website_button = QPushButton("Go to T.A.R.A.L.L.O.")
		self.website_button.setStyleSheet(button_style)
		self.website_button.clicked.connect(lambda: sp.Popen(["firefox", "127.0.0.1:8080"]))

		h_buttons.addWidget(self.clipboard_button, alignment=Qt.AlignCenter)
		h_buttons.addWidget(self.website_button, alignment=Qt.AlignCenter)

		v_box.addLayout(h_buttons)

		# if system_info is empty
		if not system_info:
			nothing_found = QLabel("Nothing was found.")
			v_box.addWidget(nothing_found, alignment=Qt.AlignCenter)

		for i, component in enumerate(system_info):
			if i == 0:
				prev_type = component["type"]
			else:
				prev_type = system_info[i - 1]["type"]

			if component["type"] != prev_type or i == 0:
				title = QLabel(component["type"].upper())
				# noinspection PyArgumentList
				title.setFont(QFont("futura", pointSize=16, italic=False))
				if i != 0:
					v_box.addSpacing(10)
				v_box.addWidget(title, alignment=Qt.AlignCenter)

			for feature in component.items():
				if feature[0] != "type":
					h_box = QHBoxLayout()

					# the single dict entry is converted to a tuple
					name = QLabel(str(feature[0]))
					if feature[1] != "":
						# skip not human readable frequency and capacity
						if feature[0] == "frequency-hertz" or feature[0] == "capacity-byte":
							continue
						elif feature[0] == "human_readable_frequency":
							name = QLabel("frequency")
						elif feature[0] == "human_readable_capacity":
							name = QLabel("capacity")
						desc = QLabel(str(feature[1]))
					else:
						desc = QLabel("missing feature")
						name.setStyleSheet("color: yellow")
						desc.setStyleSheet("color: yellow")

					h_box.addWidget(name, alignment=Qt.AlignCenter)
					h_box.addStretch()
					h_box.addWidget(desc, alignment=Qt.AlignCenter)

					v_box.addLayout(h_box)

			v_box.addSpacing(15)

		self.setLayout(v_box)


class VerifyExtractedDataScrollable(QScrollArea):
	def __init__(self, window: QMainWindow, system_info):
		super().__init__()
		self.the_widget: VerifyExtractedData = VerifyExtractedData(window, system_info)
		self.init_ui(window, self.the_widget, system_info)

	def init_ui(self, window: QMainWindow, the_widget: VerifyExtractedData, system_info):
		scroll_area = self
		scroll_area.setWidget(the_widget)
		scroll_area.setWidgetResizable(True)


def main():
	app = QApplication(sys.argv)

	# set SUPERIOR dark theme
	app.setStyle('Fusion')
	palette = QPalette()
	palette.setColor(QPalette.Window, QColor(53, 53, 53))
	palette.setColor(QPalette.WindowText, Qt.white)
	palette.setColor(QPalette.Base, QColor(15, 15, 15))
	palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
	palette.setColor(QPalette.ToolTipBase, Qt.white)
	palette.setColor(QPalette.ToolTipText, Qt.white)
	palette.setColor(QPalette.Text, Qt.white)
	palette.setColor(QPalette.Button, QColor(53, 53, 53))
	palette.setColor(QPalette.ButtonText, Qt.white)
	palette.setColor(QPalette.BrightText, Qt.red)
	palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
	palette.setColor(QPalette.HighlightedText, Qt.black)

	app.setPalette(palette)
	Window()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
