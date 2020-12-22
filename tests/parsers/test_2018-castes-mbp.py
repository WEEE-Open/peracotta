#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'tests/2018-castes-mbp/'


def test_lspci():
	expect = {
		'type': 'graphics-card',
		"working": "yes",
		'brand-manufacturer': 'AMD/ATI',
		'brand': 'Apple Inc. Radeon Pro 560X',
		'internal-name': '',
		'model': 'Radeon RX 460/560D / Pro 450/455/460/555/555X/560/560X',
		'capacity-byte': 4294967296,
		'human_readable_capacity': '4096 MB'
	}
	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(True, os.path.join(filedir, 'lspci.txt'), os.path.join(filedir, 'glxinfo.txt'))

	assert output == expect


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-64",
		"model": "Core i7-8750H",
		"brand": "Intel",
		"core-n": 6,
		"thread-n": 12,
		"frequency-hertz": 2200000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu.read_lscpu(os.path.join(filedir, 'lscpu.txt'))

	assert output == expect


def test_ram():
	output = read_decode_dimms.read_decode_dimms(os.path.join(filedir, 'dimms.txt'))

	assert len(output) == 0


def test_baseboard():
	expect = {
		'type': 'motherboard',
		"working": "yes",
		'brand': 'Apple Inc.',
		'model': 'Mac-937A206F2EE63C01',
		'sn': 'C0290440002JP5P1T'
	}
	output = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	expect = {
		'type': 'motherboard',
		"working": "yes",
		'brand': 'Apple Inc.',
		'model': 'Mac-937A206F2EE63C01',
		'sn': 'C0290440002JP5P1T',
		'usb-ports-n': 2,
		'mini-jack-ports-n': 1,
		'thunderbolt-ports-n': 1,
		'notes': '',
	}
	output = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	assert output == expect


def test_chassis():
	expect = {
		'brand': 'Apple Inc.',
		'sn': 'CENSORED',
		'type': 'case',
		'motherboard-form-factor': 'proprietary-laptop',
		'model': '',
	}
	output = read_dmidecode.get_chassis(os.path.join(filedir, 'chassis.txt'))

	assert output == expect


def test_smartctl():
	expect = []
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
