# Highly experimental makefile

COMMON ::= peracommon.py prettyprinter.py assets parsers scripts venv

.PHONY: all

all: peracotta.bin peracruda.bin

venv:
	python -m venv venv
	venv/bin/python -m pip install -r requirements-dev.txt

peracotta.bin: peracotta $(COMMON)
	venv/bin/python -m nuitka --standalone --onefile --enable-plugin=pyqt5 peracotta

peracruda.bin: peracruda $(COMMON)
	venv/bin/python -m nuitka --standalone --onefile --enable-plugin=pyqt5 peracruda
