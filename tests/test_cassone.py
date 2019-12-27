#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'cassone/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "SiS",
		'internal-name': '',
		"model": "65x/M650/740",
		"capacity-byte": None,
		"human_readable_capacity": ""
	}

	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert output == expect


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-32",
		"model": "Athlon 4",
		"brand": "AMD",
		"core-n": 1,
		"thread-n": 1,
		"frequency-hertz": -1,
		"human_readable_frequency": "N/A"
	}

	output = read_lscpu.read_lscpu(filedir + 'lscpu.txt')

	assert output == expect


def test_baseboard():
	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "Matsonic",
		"model": "MS8318E",
		"sn": "00000000",
	}
	output = read_dmidecode.get_baseboard(filedir + 'baseboard.txt')

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "Matsonic",
		"model": "MS8318E",
		"sn": "00000000",
		"parallel-ports-n": 1,
		"notes": ""
	}

	output = read_dmidecode.get_connectors(filedir + 'connector.txt', baseboard)

	assert output == expect


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Matsonic",
		"model": "",
		"sn": "00000000",
		"motherboard-form-factor": ""
	}

	output = read_dmidecode.get_chassis(filedir + 'chassis.txt')

	assert output == expect


def test_smartctl():
	output = read_smartctl.read_smartctl(filedir)

	assert 0 == len(output)
