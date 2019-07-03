#!/usr/bin/env python3

from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = '77/'


def test_77_lspci():
	expect = {
		'type': 'graphics-card',
		'brand-manufacturer': 'SiS',
		'brand': 'ASUSTeK Computer Inc.',
		'model': '771/671',
		'capacity-byte': None,
		'human_readable_capacity': ''}
	output = read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		'type': 'cpu',
		'architecture': 'x86-32',
		'model': 'Celeron 2.80GHz',
		'brand': 'Intel',
		'core-n': 1,
		'thread-n': 1,
		'frequency-hertz': -1,
		'human_readable_frequency': 'N/A'
	}
	output = read_lscpu(filedir + 'lscpu.txt')


def test_77_baseboard():
	expect = {
		'brand': 'ASUSTeK Computer INC.',
		'model': 'P5SD2-VM',
		'sn': 'MT721CT11114269',
		'type': 'motherboard'
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_77_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		'brand': 'ASUSTeK Computer INC.',
		'model': 'P5SD2-VM',
		'sn': 'MT721CT11114269',
		'type': 'motherboard',
		'usb-ports-n': 8,
		'ethernet-ports-n': 1,
		'mini-jack-ports-n': 3,
		'parallel-ports-n': 1,
		'ps2-ports-n': 2,
		'serial-ports-n': 1,
		'ide-ports-n': 3,
		'warning': 'Unknown connector: Other / None (AAFP / Not Specified)'
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_77_chassis():
	expect = {
		'brand': 'Chassis Manufacture',
		'model': '',
		'sn': 'Chassis Serial Number',
		'type': 'case',
		'motherboard-form-factor': '',
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output
