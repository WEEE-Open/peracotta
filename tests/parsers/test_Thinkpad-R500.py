#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'tests/Thinkpad-R500/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "Lenovo",
		"model": "Mobile 4 Series Chipset",
		"internal-name": "",
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
		"model": "Core 2 Duo P8600",
		"brand": "Intel",
		"core-n": 2,
		"thread-n": 2,
		"frequency-hertz": 2400000000,
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
		"brand": "LENOVO",
		"model": "2718V8C",
		"sn": "VQ1FF05G1WA",
	}
	output = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "LENOVO",
		"model": "2718V8C",
		"sn": "VQ1FF05G1WA",
		"usb-ports-n": 3,
		"vga-ports-n": 1,
		"mini-jack-ports-n": 2,
		"ethernet-ports-n": 1,
		"firewire-ports-n": 1,
		"rj11-ports-n": 1,
		"notes": ""
	}
	output = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	assert output == expect


def test_chassis():
	expect = {
		"type": "case",
		"brand": "LENOVO",
		"model": "",
		"sn": "Not Available",
		"motherboard-form-factor": "proprietary-laptop"
	}
	output = read_dmidecode.get_chassis(os.path.join(filedir, 'chassis.txt'))

	assert output == expect


def test_smartctl():
	expect = [
		{
			"type": "hdd",
			"brand": "Fujitsu",
			"model": "MJA2160BH G2",
			"family": "MJA BH",
			"wwn": "5 00000e 0447dfa8d",
			"sn": "K95BTA42BD8H",
			"capacity-decibyte": 160000000000,
			"human_readable_capacity": "160 GB",
			"spin-rate-rpm": 5400,
			"smart-data": "ok",
			'sata-ports-n': 1,
			'notes': "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR--   100   100   046    -    50270\n  2 Throughput_Performance  P-S---   100   100   030    -    25231360\n  3 Spin_Up_Time            PO----   100   100   025    -    0\n  4 Start_Stop_Count        -O--CK   099   099   000    -    3215\n  5 Reallocated_Sector_Ct   PO--CK   100   100   024    -    0 (2100 0)\n  7 Seek_Error_Rate         POSR--   100   100   047    -    1565\n  8 Seek_Time_Performance   P-S---   100   100   019    -    0\n  9 Power_On_Hours          -O--CK   088   088   000    -    6251\n 10 Spin_Retry_Count        PO--C-   100   100   020    -    0\n 12 Power_Cycle_Count       -O--CK   100   100   000    -    3007\n192 Power-Off_Retract_Count -O--CK   100   100   000    -    85\n193 Load_Cycle_Count        -O--CK   100   100   000    -    19460\n194 Temperature_Celsius     -O---K   100   100   000    -    33 (Min/Max 9/45)\n195 Hardware_ECC_Recovered  -O-RC-   100   100   000    -    185\n196 Reallocated_Event_Count -O--CK   100   100   000    -    0 (0 15680)\n197 Current_Pending_Sector  -O--C-   100   100   000    -    0\n198 Offline_Uncorrectable   ----C-   100   100   000    -    0\n199 UDMA_CRC_Error_Count    -OSRCK   200   253   000    -    1\n200 Multi_Zone_Error_Rate   POSR--   100   100   060    -    15690\n203 Run_Out_Cancel          -O----   100   100   000    -    1529060392964\n240 Head_Flying_Hours       -OSRCK   200   200   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning",
			"hdd-form-factor": "2.5-7mm"
		}
	]
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
