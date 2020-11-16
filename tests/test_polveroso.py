#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'tests/polveroso/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "ASUSTeK Computer Inc.",
		"model": "GeForce 9400 GT",
		"internal-name": "G96",
		"capacity-byte": None,  # Missing glxinfo...
		"human_readable_capacity": "",
		"brand-manufacturer": "Nvidia"
	}
	# False to ignore missing glxinfo
	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert output == expect


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-64",
		"model": "Core 2 Duo E7300",
		"brand": "Intel",
		"core-n": 2,
		"thread-n": 2,
		"frequency-hertz": 2660000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu.read_lscpu(filedir + 'lscpu.txt')

	assert output == expect


def test_ram():
	output = read_decode_dimms.read_decode_dimms(filedir + 'dimms.txt')

	assert len(output) == 0


def test_baseboard():
	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P5QL-E",
		"sn": "MS666999ABCDEF123",
	}
	output = read_dmidecode.get_baseboard(filedir + 'baseboard.txt')

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P5QL-E",
		"sn": "MS666999ABCDEF123",
		"ps2-ports-n": 2,
		"usb-ports-n": 6,
		"serial-ports-n": 1,
		"mini-jack-ports-n": 1,
		"ethernet-ports-n": 1,
		"ide-ports-n": 1,
		"sata-ports-n": 6,
		'esata-ports-n': 1,
		"firewire-ports-n": 2,
		"notes": "Unknown connector: None / Other (AUDIO / AUDIO)"
	}
	output = read_dmidecode.get_connectors(filedir + 'connector.txt', baseboard)

	assert output == expect


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Chassis Manufacture",
		"model": "",
		"sn": "Chassis Serial Number",
		"motherboard-form-factor": ""
	}
	output = read_dmidecode.get_chassis(filedir + 'chassis.txt')

	assert output == expect


def test_smartctl():
	expect = []
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
