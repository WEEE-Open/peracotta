#!/usr/bin/env python3

from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = '77/'


def test_77_lspci():
	expect = {
		'type': 'graphics-card',
		"working": "yes",
		'brand-manufacturer': 'SiS',
		'brand': 'ASUSTeK Computer Inc.',
		'internal-name': '',
		'model': '771/671',
		'capacity-byte': None,
		'human_readable_capacity': ''}
	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert output == expect


def test_lscpu():
	expect = {
		'type': 'cpu',
		"working": "yes",
		'isa': 'x86-32',
		'model': 'Celeron 2.80GHz',
		'brand': 'Intel',
		'core-n': 1,
		'thread-n': 1,
		'frequency-hertz': -1,
		'human_readable_frequency': 'N/A'
	}
	output = read_lscpu.read_lscpu(filedir + 'lscpu.txt')


def test_77_baseboard():
	expect = {
		'brand': 'ASUSTeK Computer INC.',
		'model': 'P5SD2-VM',
		'sn': 'MT721CT11114269',
		'type': 'motherboard',
		"working": "yes",
	}
	output = read_dmidecode.get_baseboard(filedir + 'baseboard.txt')

	assert output == expect


def test_77_connector():
	baseboard = read_dmidecode.get_baseboard(filedir + 'baseboard.txt')

	expect = {
		'brand': 'ASUSTeK Computer INC.',
		'model': 'P5SD2-VM',
		'sn': 'MT721CT11114269',
		'type': 'motherboard',
		"working": "yes",
		'usb-ports-n': 8,
		'ethernet-ports-n': 1,
		'mini-jack-ports-n': 3,
		'parallel-ports-n': 1,
		'ps2-ports-n': 2,
		'serial-ports-n': 1,
		'ide-ports-n': 1,
		'sata-ports-n': 2,
		'notes': 'Unknown connector: Other / None (AAFP / Not Specified)'
	}
	output = read_dmidecode.get_connectors(filedir + 'connector.txt', baseboard)

	assert output == expect


def test_77_chassis():
	expect = {
		'brand': 'Chassis Manufacture',
		'model': '',
		'sn': 'Chassis Serial Number',
		'type': 'case',
		'motherboard-form-factor': '',
	}
	output = read_dmidecode.get_chassis(filedir + 'chassis.txt')

	assert output == expect
