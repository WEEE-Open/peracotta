#!/usr/bin/env python3
import os

from parsers import read_lscpu
from parsers import read_smartctl
import os

filedir = 'tests/77-no-disks/'


def test_lscpu():
	expect = {
		'type': 'cpu',
		"working": "yes",
		'isa': 'x86-32',
		'model': 'Celeron 2.80GHz',
		'brand': 'Intel',
		'core-n': 1,
		'thread-n': 1,
		'frequency-hertz': 2800000000,
	}
	output = read_lscpu.read_lscpu(os.path.join(filedir, 'lscpu.txt'))

	assert output == expect


def test_77_no_disks_disk_that_doesnt_exist():
	expect = []
	output = read_smartctl.read_smartctl(os.path.join(filedir))

	assert output == expect
