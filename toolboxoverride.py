#!/usr/bin/env python3

# This file has to be a separate file, it's mandatory, it cannot be moved anywhere else.
# The reason is: uic is doing some dark magic
# https://stackoverflow.com/a/19622817

from PyQt5 import QtWidgets, QtCore


class ToolBoxOverride(QtWidgets.QToolBox):
    def __init__(self, parent):
        super().__init__(parent)

    def minimumSizeHint(self) -> QtCore.QSize:
        h = 0
        for child in self.children():
            if isinstance(child, QtWidgets.QScrollArea):
                if child.isHidden():
                    h += child.minimumSizeHint().height()
                else:
                    h += child.sizeHint().height()
            elif isinstance(child, QtWidgets.QWidget):
                # print(f"{child}: {child.sizeHint().height()} vs {child.minimumSizeHint().height()}")
                # Buttons and anything else
                h += child.sizeHint().height()
        old = super().minimumSizeHint()
        if h > old.height():
            old.setHeight(h)
        return old

