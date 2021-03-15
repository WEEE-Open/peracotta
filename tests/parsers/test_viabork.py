#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'tests/viabork/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "ASUSTeK Computer Inc.",
		"model": "S3 UniChrome Pro",
		"internal-name": "P4M890",
		"capacity-byte": None,
		"brand-manufacturer": "VIA"
	}
	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(False, os.path.join(filedir, 'lspci.txt'), os.path.join(filedir, 'glxinfo.txt'))

	assert output == expect


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-64",
		"model": "Pentium 4 3.00GHz",
		"brand": "Intel",
		"core-n": 1,
		"thread-n": 2,
		"frequency-hertz": 3000000000,
	}
	output = read_lscpu.read_lscpu(os.path.join(filedir, 'lscpu.txt'))

	assert output == expect


def test_ram():
	output = read_decode_dimms.read_decode_dimms(os.path.join(filedir, 'dimms.txt'))

	assert len(output) == 0


def test_baseboard():
	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P5V-VM-ULTRA",
		"sn": "MB-1234567890",
	}
	output = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P5V-VM-ULTRA",
		"sn": "MB-1234567890",
		"ps2-ports-n": 2,
		"usb-ports-n": 8,
		"parallel-ports-n": 1,
		"serial-ports-n": 1,
		"mini-jack-ports-n": 3,
		"ethernet-ports-n": 1,
		"ide-ports-n": 2,
		"notes": ""
	}
	output = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	assert output == expect


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Chassis Manufacture",
		"model": "",
		"sn": "Chassis Serial Number",
		"motherboard-form-factor": ""
	}
	output = read_dmidecode.get_chassis(os.path.join(filedir, 'chassis.txt'))

	assert output == expect


def test_smartctl():
	expect = []
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
