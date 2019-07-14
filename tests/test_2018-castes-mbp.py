#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = '2018-castes-mbp/'


def test_lspci():
	expect = {
		'type': 'graphics-card',
		'brand-manufacturer': 'AMD/ATI',
		'brand': 'Apple Inc. Radeon Pro 560X',
		'internal-name': '',
		'model': 'Radeon RX 460/560D / Pro 450/455/460/555/555X/560/560X',
		'capacity-byte': 4294967296,
		'human_readable_capacity': '4096 MB'
	}
	output = read_lspci_and_glxinfo(True, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"isa": "x86-64",
		"model": "Core i7-8750H",
		"brand": "Intel",
		"core-n": 6,
		"thread-n": 12,
		"frequency-hertz": 2200000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu(filedir + 'lscpu.txt')

	assert expect == output


def test_ram():
	output = read_decode_dimms(filedir + 'dimms.txt')

	assert len(output) == 0


def test_baseboard():
	expect = {
		'type': 'motherboard',
		'brand': 'Apple Inc.',
		'model': 'Mac-937A206F2EE63C01',
		'sn': '***REMOVED***'
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		'type': 'motherboard',
		'brand': 'Apple Inc.',
		'model': 'Mac-937A206F2EE63C01',
		'sn': '***REMOVED***',
		'usb-ports-n': 2,
		'mini-jack-ports-n': 1,
		'thunderbolt-ports-n': 1,
		'notes': '',
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	expect = {
		'brand': 'Apple Inc.',
		'sn': 'CENSORED',
		'type': 'case',
		'motherboard-form-factor': 'proprietary-laptop',
		'model': '',
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


def test_smartctl():
	expect = []
	output = read_smartctl(filedir)

	assert expect == output
