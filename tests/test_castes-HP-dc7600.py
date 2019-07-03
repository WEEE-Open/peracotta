#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'castes-HP-dc7600/'


def test_lspci_dedicated():
	expect = {
		'type': 'graphics-card',
		'brand': 'PC Partner Limited / Sapphire Technology G98',
		'model': 'GeForce G 100',
		'capacity-byte': 520093696,
		'human_readable_capacity': '496 MB',
		'brand-manufacturer': 'Nvidia'
	}
	output = read_lspci_and_glxinfo(True, filedir + 'NVIDIA-G100/lspci.txt', filedir + 'NVIDIA-G100/glxinfo.txt')

	assert expect == output


def test_lspci_integrated():
	expect = {
		'type': 'graphics-card',
		'brand': 'Hewlett-Packard Company',
		'model': '82945G/GZ',
		'capacity-byte': None,
		'human_readable_capacity': '',
		'brand-manufacturer': 'Intel'
	}
	output = read_lspci_and_glxinfo(False, filedir + '82945G/lspci.txt', filedir + '82945G/glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"architecture": "x86-32",
		"model": "Pentium 4 2.80GHz",
		"brand": "Intel",
		"core-n": 1,
		"thread-n": 2,
		"frequency-hertz": 2800000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu(filedir + 'lscpu.txt')

	assert expect == output


def test_ram():
	output = read_decode_dimms(filedir + 'dimms.txt')

	assert len(output) == 0


def test_baseboard():
	expect = {
		"type": "motherboard",
		"brand": "Hewlett-Packard",
		"model": "09F8h",
		"sn": "CZC6203MC5",
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
		"brand": "Hewlett-Packard",
		"model": "09F8h",
		"sn": "CZC6203MC5",
		"ps2-ports-n": 2,
		"usb-ports-n": 8,
		"serial-ports-n": 2,
		"ethernet-ports-n": 1,
		"ide-ports-n": 1,
		"warning": "Unknown connector: Other / None (SATA0 / Not Specified)\nUnknown connector: Other / None (SATA1 / Not Specified)\nUnknown connector: None / DB-25 female (Not Specified / PARALLEL)\nUnknown connector: None / Mini DIN (Not Specified / REAR LINE IN)\nUnknown connector: None / DB-15 female (Not Specified / VIDEO)\nUnknown connector: None / Mini DIN (Not Specified / REAR HEADPHONE/LINEOUT)\nUnknown connector: Other / None (CPU FAN / Not Specified)\nUnknown connector: Other / Mini DIN (FRNT AUD / FRONT HEADPHONE/LINEOUT & MIC)\nUnknown connector: Other / None (CHASSIS FAN / Not Specified)\nUnknown connector: Other / None (SPEAKER (SPKR) / Not Specified)\nUnknown connector: Other / None (PASSWORD CLEAR (PSWD) / Not Specified)\nUnknown connector: Other / None (HOOD SENSE (HSENSE) / Not Specified)\nUnknown connector: Other / None (HOOD LOCK (HLCK) / Not Specified)\nUnknown connector: Other / None (TPM SECURITY (SEC) / Not Specified)"
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Hewlett-Packard",
		"model": "",
		"sn": "CZC6203MC5",
		"motherboard-form-factor": ""
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output