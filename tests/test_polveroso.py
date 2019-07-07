#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'polveroso/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"brand": "ASUSTeK Computer Inc.",
		"model": "GeForce 9400 GT",
		"internal-name": "G96",
		"capacity-byte": -1,  # Missing glxinfo...
		"human_readable_capacity": "",
		"brand-manufacturer": "Nvidia"
	}
	output = read_lspci_and_glxinfo(True, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"architecture": "x86-64",
		"model": "Core 2 Duo E7300",
		"brand": "Intel",
		"core-n": 2,
		"thread-n": 2,
		"frequency-hertz": 2660000000,
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
		"brand": "ASUSTeK Computer INC.",
		"model": "P5QL-E",
		"sn": "MS666999ABCDEF123",
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
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
		"firewire-ports-n": 2,
		"notes": "Unknown connector: None / Other (AUDIO / AUDIO)\nUnknown connector: SAS/SATA Plug Receptacle / None (ESATA / Not Specified)"
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Chassis Manufacture",
		"model": "",
		"sn": "Chassis Serial Number",
		"motherboard-form-factor": ""
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


def test_smartctl():
	expect = []
	output = read_smartctl(filedir)

	assert expect == output
