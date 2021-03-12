#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'tests/dismone/'


def test_lspci():
	# no glxinfo :(
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "ASUSTeK Computer Inc.",
		"model": "GeForce GTX 970",
		'internal-name': 'GM204',
		"capacity-byte": None,
		"human_readable_capacity": "",
		"brand-manufacturer": "Nvidia"
	}
	# False to ignore missing glxinfo
	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(False, os.path.join(filedir, 'lspci.txt'), os.path.join(filedir, 'glxinfo.txt'))

	assert output == expect


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-64",
		"model": "Core i7 930",
		"brand": "Intel",
		"core-n": 4,
		"thread-n": 8,
		"frequency-hertz": 2800000000,
		"human_readable_frequency": "2.80 GHz"
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
		"model": "P6T DELUXE V2",
		"sn": "723627130020069",
	}
	output = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P6T DELUXE V2",
		"sn": "723627130020069",
		"ps2-ports-n": 1,
		"usb-ports-n": 7,
		'firewire-ports-n': 3,
		'ide-ports-n': 1,
		'sata-ports-n': 6,
		"mini-jack-ports-n": 7,
		"ethernet-ports-n": 2,
		'sas-sata-ports-n': 2,
		'notes': 'Unknown connector: None / Other (AUDIO / AUDIO)'
	}
	output = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	assert output == expect


def test_net_without_connectors():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P6T DELUXE V2",
		"sn": "723627130020069",
		'ethernet-ports-1000m-n': 2,
		'mac': '00:c0:11:fe:fe:11, 00:c0:11:fe:fe:22',
	}
	output = read_dmidecode.get_net(os.path.join(filedir, 'net.txt'), baseboard)

	assert output == expect


def test_net_with_connectors():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))
	baseboard = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P6T DELUXE V2",
		"sn": "723627130020069",
		"ps2-ports-n": 1,
		"usb-ports-n": 7,
		'firewire-ports-n': 3,
		'ide-ports-n': 1,
		'sata-ports-n': 6,
		"mini-jack-ports-n": 7,
		'ethernet-ports-1000m-n': 2,
		'mac': '00:c0:11:fe:fe:11, 00:c0:11:fe:fe:22',
		'sas-sata-ports-n': 2,
		'notes': 'Unknown connector: None / Other (AUDIO / AUDIO)'
	}
	output = read_dmidecode.get_net(os.path.join(filedir, 'net.txt'), baseboard)

	assert output == expect


def test_net_with_connectors_different():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))
	baseboard = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P6T DELUXE V2",
		"sn": "723627130020069",
		"ps2-ports-n": 1,
		"usb-ports-n": 7,
		'firewire-ports-n': 3,
		'ide-ports-n': 1,
		'sata-ports-n': 6,
		"mini-jack-ports-n": 7,
		'ethernet-ports-1000m-n': 1,
		'ethernet-ports-100m-n': 1,
		'mac': '00:c0:11:fe:fe:11, 00:c0:11:fe:fe:22',
		'sas-sata-ports-n': 2,
		'notes': 'Unknown connector: None / Other (AUDIO / AUDIO)'
	}
	output = read_dmidecode.get_net(os.path.join(filedir, 'net_different.txt'), baseboard)

	assert output == expect


def test_net_with_connectors_too_few():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))
	baseboard = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P6T DELUXE V2",
		"sn": "723627130020069",
		"ps2-ports-n": 1,
		"usb-ports-n": 7,
		'firewire-ports-n': 3,
		'ide-ports-n': 1,
		'sata-ports-n': 6,
		"mini-jack-ports-n": 7,
		'ethernet-ports-1000m-n': 1,
		'mac': '00:c0:11:fe:fe:22',
		'sas-sata-ports-n': 2,
		'notes': 'Unknown connector: None / Other (AUDIO / AUDIO)\n'
			'BIOS reported 1 more ethernet port that was not found by the kernel'
	}
	output = read_dmidecode.get_net(os.path.join(filedir, 'net_too_few.txt'), baseboard)

	assert output == expect


def test_net_with_connectors_too_many():
	baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, 'baseboard.txt'))
	baseboard = read_dmidecode.get_connectors(os.path.join(filedir, 'connector.txt'), baseboard)

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P6T DELUXE V2",
		"sn": "723627130020069",
		"ps2-ports-n": 1,
		"usb-ports-n": 7,
		'firewire-ports-n': 3,
		'ide-ports-n': 1,
		'sata-ports-n': 6,
		"mini-jack-ports-n": 7,
		'ethernet-ports-1000m-n': 3,
		'mac': '00:c0:11:fe:fe:11, 00:c0:11:fe:fe:22, 00:c0:11:fe:fe:42',
		'sas-sata-ports-n': 2,
		'notes': 'Unknown connector: None / Other (AUDIO / AUDIO)'
	}
	output = read_dmidecode.get_net(os.path.join(filedir, 'net_too_many.txt'), baseboard)

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
	expect = [
		{
			"type": "hdd",
			"brand": "Western Digital",
			"model": "WD5002ABYS-02B1B0",
			"family": "RE3 Serial ATA",
			"wwn": "5 0014ee 7bf4d152d",
			"sn": "WCASYD636342",
			"capacity-decibyte": 500000000000,
			"human_readable_capacity": "500 GB",
			"spin-rate-rpm": 7200,
			"smart-data": "ok",
			'sata-ports-n': 1,
			'notes': "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR-K   200   200   051    -    0\n  3 Spin_Up_Time            POS--K   239   230   021    -    1016\n  4 Start_Stop_Count        -O--CK   100   100   000    -    227\n  5 Reallocated_Sector_Ct   PO--CK   200   200   140    -    0\n  7 Seek_Error_Rate         -OSR-K   200   200   000    -    0\n  9 Power_On_Hours          -O--CK   035   035   000    -    47525\n 10 Spin_Retry_Count        -O--CK   100   100   000    -    0\n 11 Calibration_Retry_Count -O--CK   100   100   000    -    0\n 12 Power_Cycle_Count       -O--CK   100   100   000    -    224\n192 Power-Off_Retract_Count -O--CK   200   200   000    -    72\n193 Load_Cycle_Count        -O--CK   200   200   000    -    154\n194 Temperature_Celsius     -O---K   116   104   000    -    31\n196 Reallocated_Event_Count -O--CK   200   200   000    -    0\n197 Current_Pending_Sector  -O--CK   200   200   000    -    0\n198 Offline_Uncorrectable   ----CK   200   200   000    -    0\n199 UDMA_CRC_Error_Count    -O--CK   200   200   000    -    0\n200 Multi_Zone_Error_Rate   ---R--   200   200   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning"
		},
		{
			"type": "hdd",
			"brand": "Western Digital",
			"model": "WD5002ABYS-02B1B0",
			"family": "RE3 Serial ATA",
			"wwn": "5 0014ee 3ef215d89",
			"sn": "WCASYE636777",
			"capacity-decibyte": 500000000000,
			"human_readable_capacity": "500 GB",
			"spin-rate-rpm": 7200,
			"smart-data": "ok",
			'sata-ports-n': 1,
			'notes': "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR-K   200   200   051    -    0\n  3 Spin_Up_Time            POS--K   239   228   021    -    1033\n  4 Start_Stop_Count        -O--CK   100   100   000    -    228\n  5 Reallocated_Sector_Ct   PO--CK   200   200   140    -    0\n  7 Seek_Error_Rate         -OSR-K   200   200   000    -    0\n  9 Power_On_Hours          -O--CK   044   044   000    -    41574\n 10 Spin_Retry_Count        -O--CK   100   100   000    -    0\n 11 Calibration_Retry_Count -O--CK   100   100   000    -    0\n 12 Power_Cycle_Count       -O--CK   100   100   000    -    224\n192 Power-Off_Retract_Count -O--CK   200   200   000    -    72\n193 Load_Cycle_Count        -O--CK   200   200   000    -    155\n194 Temperature_Celsius     -O---K   116   105   000    -    31\n196 Reallocated_Event_Count -O--CK   200   200   000    -    0\n197 Current_Pending_Sector  -O--CK   200   200   000    -    0\n198 Offline_Uncorrectable   ----CK   200   200   000    -    0\n199 UDMA_CRC_Error_Count    -O--CK   200   200   000    -    0\n200 Multi_Zone_Error_Rate   ---R--   200   200   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning"
		}
	]
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
