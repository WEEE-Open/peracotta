#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'tests/jm11/'


def test_lspci():
	# VGA core graphics processor core VGA processor graphics core VGA processor is the core of this laptop
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "Lenovo 3rd Gen Core processor Graphics Controller",
		"model": "VGA controller",
		"internal-name": "",
		"capacity-byte": None,
		"brand-manufacturer": "Intel"
	}
	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(False, os.path.join(filedir, 'lspci.txt'), os.path.join(filedir, 'glxinfo.txt'))

	assert output == expect


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-64",
		"model": "Core i5-3210M",
		"brand": "Intel",
		"core-n": 2,
		"thread-n": 4,
		"frequency-hertz": 2500000000,
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
		"model": "246837G",
		"sn": "2RTC1A0N333",
	}
	output = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "LENOVO",
		"model": "246837G",
		"sn": "2RTC1A0N333",
		"usb-ports-n": 4,
		"vga-ports-n": 1,
		"mini-jack-ports-n": 1,
		"ethernet-ports-n": 1,
		"mini-displayport-ports-n": 1,
		"notes": "",
	}
	output = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	assert output == expect


def test_chassis():
	expect = {
		"type": "case",
		"brand": "LENOVO",
		"model": "",
		"sn": "A2K3GED",
		"motherboard-form-factor": "proprietary-laptop"
	}
	output = read_dmidecode.get_chassis(os.path.join(filedir, 'chassis.txt'))

	assert output == expect


def test_smartctl():
	expect = [
		{
			"type": "ssd",
			"brand": "Crucial",
			"model": "CT128M550SSD3",
			"family": "MX100/MX200/M5x0/M600 Client SSDs",
			"sn": "14110C323F00",
			'wwn': '5 00a075 01d3243de',
			"capacity-byte": 128000000000,
			'smart-data': 'ok',
			'sata-ports-n': 1, # TODO: this is wrong, this is mSATA
			"notes": "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR-K   100   100   000    -    2\n  5 Reallocate_NAND_Blk_Cnt PO--CK   100   100   000    -    0\n  9 Power_On_Hours          -O--CK   100   100   000    -    4767\n 12 Power_Cycle_Count       -O--CK   100   100   000    -    7869\n171 Program_Fail_Count      -O--CK   100   100   000    -    0\n172 Erase_Fail_Count        -O--CK   100   100   000    -    0\n173 Ave_Block-Erase_Count   -O--CK   095   095   000    -    177\n174 Unexpect_Power_Loss_Ct  -O--CK   100   100   000    -    366\n180 Unused_Reserve_NAND_Blk PO--CK   000   000   000    -    1036\n183 SATA_Interfac_Downshift -O--CK   100   100   000    -    0\n184 Error_Correction_Count  -O--CK   100   100   000    -    0\n187 Reported_Uncorrect      -O--CK   100   100   000    -    0\n194 Temperature_Celsius     -O---K   034   006   000    -    66 (Min/Max 17/94)\n196 Reallocated_Event_Count -O--CK   100   100   000    -    0\n197 Current_Pending_Sector  -O--CK   100   100   000    -    0\n198 Offline_Uncorrectable   ----CK   100   100   000    -    0\n199 UDMA_CRC_Error_Count    -O--CK   100   100   000    -    0\n202 Percent_Lifetime_Used   P---CK   095   095   000    -    5\n206 Write_Error_Rate        -OSR--   100   100   000    -    0\n210 Success_RAIN_Recov_Cnt  -O--CK   100   100   000    -    0\n246 Total_Host_Sector_Write -O--CK   100   100   000    -    14546033643\n247 Host_Program_Page_Count -O--CK   100   100   000    -    463669262\n248 Bckgnd_Program_Page_Cnt -O--CK   100   100   000    -    910054629\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning"
		}
	]
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
