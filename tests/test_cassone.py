#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'cassone/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"brand": "SiS",
		'internal-name': '',
		"model": "65x/M650/740",
		"capacity-byte": None,
		"human_readable_capacity": ""
	}

	output = read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"architecture": "x86-32",
		"model": "Athlon 4",
		"brand": "AMD",
		"core-n": 1,
		"thread-n": 1,
		"frequency-hertz": -1,
		"human_readable_frequency": "N/A"
	}

	output = read_lscpu(filedir + 'lscpu.txt')

	assert expect == output


def test_baseboard():
	expect = {
		"type": "motherboard",
		"brand": "Matsonic",
		"model": "MS8318E",
		"sn": "00000000",
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
		"brand": "Matsonic",
		"model": "MS8318E",
		"sn": "00000000",
		"parallel-ports-n": 1,
		"notes": ""
	}

	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Matsonic",
		"model": "",
		"sn": "00000000",
		"motherboard-form-factor": ""
	}

	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


def test_smartctl():
	output = read_smartctl(filedir)

	assert 0 == len(output)
