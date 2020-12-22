#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'tests/asdpc/'


def test_lspci():
	expect = {
		'type': 'graphics-card',
		"working": "yes",
		'brand-manufacturer': 'AMD/ATI',
		'internal-name': '',
		'brand': 'PC Partner Limited / Sapphire Technology Tahiti PRO',
		'model': 'Radeon HD 7950/8950 OEM / R9 280',
		'capacity-byte': 3221225472,
		'human_readable_capacity': '3072 MB'
	}
	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(True, os.path.join(filedir, 'lspci.txt'), os.path.join(filedir, 'glxinfo.txt'))

	assert output == expect


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-64",
		"model": "FX-8370E",
		"brand": "AMD",
		"core-n": 4,
		"thread-n": 8,
		"frequency-hertz": 3300000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu.read_lscpu(os.path.join(filedir, 'lscpu.txt'))

	assert output == expect


def test_ram():
	expect = [
		{
			'ram-ecc': 'no',
			'ram-type': 'ddr3',
			'brand': 'G Skill Intl',
			'capacity-byte': 8589934592,
			'frequency-hertz': 1333000000,
			'human_readable_capacity': '8192 MB',
			'human_readable_frequency': '1333 MHz',
			'model': 'F3-1600C7-8GTX',
			'sn': '',
			'type': 'ram',
			"working": "yes",
			'ram-timings': '9-9-9-24',
		},
		{
			'ram-ecc': 'no',
			'ram-type': 'ddr3',
			'brand': 'G Skill Intl',
			'capacity-byte': 8589934592,
			'frequency-hertz': 1333000000,
			'human_readable_capacity': '8192 MB',
			'human_readable_frequency': '1333 MHz',
			'model': 'F3-1600C7-8GTX',
			'sn': '',
			'type': 'ram',
			"working": "yes",
			'ram-timings': '9-9-9-24',
		}
	]
	output = read_decode_dimms.read_decode_dimms(os.path.join(filedir, 'dimms.txt'))

	assert len(output) == 2, "2 RAM modules are found"
	assert output == expect


def test_baseboard():
	expect = {
		'brand': 'Gigabyte Technology Co., Ltd.',
		'model': '970A-DS3P FX',
		'sn': 'To be filled by O.E.M.',
		'type': 'motherboard',
		"working": "yes",
	}
	output = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	# This is entirely wrong and is not reflected by any means from reality and the real motherboard, but the manufacturer
	# dropped all this garbage into the DMI information, so here we go...
	expect = {
		'brand': 'Gigabyte Technology Co., Ltd.',
		'model': '970A-DS3P FX',
		'sn': 'To be filled by O.E.M.',
		'type': 'motherboard',
		"working": "yes",
		'usb-ports-n': 3,
		'ps2-ports-n': 2,
		'vga-ports-n': 1,
		'serial-ports-n': 1,
		'notes': 'Unknown connector: None / Mini Centronics Type-14 (J2A1 / TV Out)\n'
					'Unknown connector: Other / None (J9A1 - TPM HDR / Not Specified)\n'
					'Unknown connector: Other / None (J9C1 - PCIE DOCKING CONN / Not Specified)\n'
					'Unknown connector: Other / None (J6C2 - EXT HDMI / Not Specified)\n'
					'Unknown connector: Other / None (J1D1 - ITP / Not Specified)\n'
					'Unknown connector: Other / None (J9E2 - MDC INTPSR / Not Specified)\n'
					'Unknown connector: Other / None (J9E4 - MDC INTPSR / Not Specified)\n'
					'Unknown connector: Other / None (J9E3 - LPC HOT DOCKING / Not Specified)\n'
					'Unknown connector: Other / None (J9E1 - SCAN MATRIX / Not Specified)\n'
					'Unknown connector: Other / None (J9G1 - LPC SIDE BAND / Not Specified)\n'
					'Unknown connector: Other / None (J8F1 - UNIFIED / Not Specified)\n'
					'Unknown connector: Other / None (J6F1 - LVDS / Not Specified)\n'
					'Unknown connector: Other / None (J2G1 - GFX VID / Not Specified)\n'
					'Unknown connector: Other / None (J1G6 - AC JACK / Not Specified)',
	}
	output = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	assert output == expect


def test_chassis():
	# This is also wrong, but for pre-assembled computers it should be right
	expect = {
		'brand': 'Gigabyte Technology Co., Ltd.',
		'model': '',
		'sn': 'To Be Filled By O.E.M.',
		'type': 'case',
		'motherboard-form-factor': '',
	}
	output = read_dmidecode.get_chassis(os.path.join(filedir, 'chassis.txt'))

	assert output == expect


def test_smartctl():
	expect = [
		{
			'type': 'ssd',
			'brand': 'Samsung',
			'family': 'based SSDs',  # whatever.
			'model': '840 EVO 120GB',
			'sn': 'S1F00F00F00F00',
			'wwn': '5 002538 2c302d451',
			'capacity-byte': 120000000000,
			'human_readable_capacity': '120 GB',
			'smart-data': 'ok',
			'sata-ports-n': 1,
			'notes': 'Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  5 Reallocated_Sector_Ct   PO--CK   100   100   010    -    0\n  9 Power_On_Hours          -O--CK   097   097   000    -    12337\n 12 Power_Cycle_Count       -O--CK   095   095   000    -    4108\n177 Wear_Leveling_Count     PO--C-   095   095   000    -    57\n179 Used_Rsvd_Blk_Cnt_Tot   PO--C-   100   100   010    -    0\n181 Program_Fail_Cnt_Total  -O--CK   100   100   010    -    0\n182 Erase_Fail_Count_Total  -O--CK   100   100   010    -    0\n183 Runtime_Bad_Block       PO--C-   100   100   010    -    0\n187 Uncorrectable_Error_Cnt -O--CK   100   100   000    -    0\n190 Airflow_Temperature_Cel -O--CK   072   058   000    -    28\n195 ECC_Error_Rate          -O-RC-   200   200   000    -    0\n199 CRC_Error_Count         -OSRCK   100   100   000    -    0\n235 POR_Recovery_Count      -O--C-   099   099   000    -    133\n241 Total_LBAs_Written      -O--CK   099   099   000    -    17500329386\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning'
		},
		{
			'type': 'hdd',
			'brand': 'Western Digital',
			'family': 'Black',
			'model': 'WD1003FZEX-00MK2A0',
			'wwn': '5 0014ee 21c4e201d',
			'sn': 'WCC3B4RB4RB4R',
			'capacity-decibyte': 1000000000000,
			'human_readable_capacity': '1,00 TB',
			'spin-rate-rpm': 7200,
			'smart-data': 'ok',
			'sata-ports-n': 1,
			'notes': 'Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR-K   200   200   051    -    0\n  3 Spin_Up_Time            POS--K   176   174   021    -    2200\n  4 Start_Stop_Count        -O--CK   094   094   000    -    6158\n  5 Reallocated_Sector_Ct   PO--CK   200   200   140    -    0\n  7 Seek_Error_Rate         -OSR-K   200   200   000    -    0\n  9 Power_On_Hours          -O--CK   084   084   000    -    12016\n 10 Spin_Retry_Count        -O--CK   100   100   000    -    0\n 11 Calibration_Retry_Count -O--CK   100   100   000    -    0\n 12 Power_Cycle_Count       -O--CK   097   097   000    -    3965\n192 Power-Off_Retract_Count -O--CK   200   200   000    -    71\n193 Load_Cycle_Count        -O--CK   198   198   000    -    6086\n194 Temperature_Celsius     -O---K   115   106   000    -    28\n196 Reallocated_Event_Count -O--CK   200   200   000    -    0\n197 Current_Pending_Sector  -O--CK   200   200   000    -    0\n198 Offline_Uncorrectable   ----CK   100   253   000    -    0\n199 UDMA_CRC_Error_Count    -O--CK   200   200   000    -    0\n200 Multi_Zone_Error_Rate   ---R--   100   253   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning'
		},
	]
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
