#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'tests/castes-SurfacePro4/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "Microsoft Corporation",
		"model": "HD Graphics 515",
		'internal-name': '',
		"capacity-byte": None,
		"human_readable_capacity": "",
		"brand-manufacturer": "Intel"
	}
	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(False, os.path.join(filedir, 'lspci.txt'), os.path.join(filedir, 'glxinfo.txt'))

	assert output == expect


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-64",
		"model": "Core m3-6Y30",
		"brand": "Intel",
		"core-n": 2,
		"thread-n": 4,
		"frequency-hertz": 900000000,
		"human_readable_frequency": "N/A"
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
		"brand": "Microsoft Corporation",
		"model": "Surface Pro 4",
		"sn": "A01012111654643A",
	}
	output = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "Microsoft Corporation",
		"model": "Surface Pro 4",
		"sn": "A01012111654643A",
		"notes": ""
	}
	output = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	assert output == expect


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Microsoft Corporation",
		"model": "",
		"sn": "CENSORED",
		"motherboard-form-factor": "proprietary-laptop"
	}
	output = read_dmidecode.get_chassis(os.path.join(filedir, 'chassis.txt'))

	assert output == expect


def test_smartctl():
	# TODO: parse this thing
	expect = [
		{
			"type": "hdd",  # Weird smarctl results here... there's no way in the file to tell this is a SSD and not an HDD
			"brand": "Samsung",
			"model": "MZFLV128HCGR-000MV",
			"family": "",
			"sn": "S244NX0H985438",
			"capacity-decibyte": -1,  # This is also wrong because whatever
			"spin-rate-rpm": -1,
			"wwn": "",
			"notes": "SMART/Health Information (NVMe Log 0x02, NSID 0x1)\nCritical Warning:                   0x00\nTemperature:                        31 Celsius\nAvailable Spare:                    100%\nAvailable Spare Threshold:          10%\nPercentage Used:                    1%\nData Units Read:                    9,622,050 [4.92 TB]\nData Units Written:                 6,340,481 [3.24 TB]\nHost Read Commands:                 128,200,306\nHost Write Commands:                69,116,853\nController Busy Time:               1,045\nPower Cycles:                       692\nPower On Hours:                     301\nUnsafe Shutdowns:                   31\nMedia and Data Integrity Errors:    0\nError Information Log Entries:      0",
			"human_readable_capacity": "",
			"smart-data": "ok",
		}
	]
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
