#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'workstation/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"brand": "ASUSTeK Computer Inc.",
		"model": "GeForce 9600 GT",
		"internal-name": "G94",
		"capacity-byte": -1,
		"human_readable_capacity": "",
		"brand-manufacturer": "Nvidia"
	}
	output = read_lspci_and_glxinfo(True, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = [
		{
			"type": "cpu",
			"isa": "x86-64",
			"model": "Xeon 5160",
			"brand": "Intel",
			"core-n": 2,
			"thread-n": 2,
			"frequency-hertz": 3000000000,
			"human_readable_frequency": "N/A"
		},
		{
			"type": "cpu",
			"isa": "x86-64",
			"model": "Xeon 5160",
			"brand": "Intel",
			"core-n": 2,
			"thread-n": 2,
			"frequency-hertz": 3000000000,
			"human_readable_frequency": "N/A"
		}
	]
	output = read_lscpu(filedir + 'lscpu.txt')

	assert isinstance(expect, list)
	assert len(expect) == 2
	assert expect == output


def test_ram():
	output = read_decode_dimms(filedir + 'dimms.txt')

	assert len(output) == 0


def test_baseboard():
	expect = {
		"type": "motherboard",
		"brand": "Dell Inc.",
		"model": "0MY171",
		"sn": "CN125321L404Q",
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
		"brand": "Dell Inc.",
		"model": "0MY171",
		"sn": "CN125321L404Q",
		"serial-ports-n": 2,
		"ps2-ports-n": 2,
		"parallel-ports-n": 1,
		"firewire-ports-n": 2,
		"usb-ports-n": 8,
		"mini-jack-ports-n": 4,
		"ethernet-ports-n": 1,
		"notes": ""
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Dell Inc.",
		"model": "",
		"sn": "5ASDL3L",
		"motherboard-form-factor": ""
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


def test_smartctl():
	# RAID managed by motherboard
	expect = [
		{
			"type": "hdd",
			"brand": "",
			"model": "",
			"family": "",
			"wwn": "",
			"sn": "",
			"capacity-decibyte": 996000000000,
			"human_readable_capacity": "995 GB",
			"spin-rate-rpm": 20000,
			"smart-data": "=== START OF READ SMART DATA SECTION ===\nCurrent Drive Temperature:     0 C\nDrive Trip Temperature:        0 C\n\nError Counter logging not supported\n\nDevice does not support Self Test logging\nDevice does not support Background scan results logging\n"
		}
	]
	output = read_smartctl(filedir)

	assert expect == output
