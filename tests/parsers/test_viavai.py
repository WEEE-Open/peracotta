#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'tests/viavai/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "ASUSTeK Computer Inc.",
		"model": "Chrome 9 HC",
		"internal-name": "CN896/VN896/P4M900",
		"capacity-byte": None,
		"human_readable_capacity": "",
		"brand-manufacturer": "VIA"
	}
	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert output == expect


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-64",
		"model": "Celeron 2.80GHz",
		"brand": "Intel",
		"core-n": 1,
		"thread-n": 1,
		"frequency-hertz": 2800000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu.read_lscpu(filedir + 'lscpu.txt')

	assert output == expect


def test_ram():
	expect = [
		{
			"type": "ram",
			"working": "yes",
			"brand": "Kingston",
			"model": "KD6502-ELG",
			"sn": "3072778780",
			"frequency-hertz": 667000000,
			"human_readable_frequency": "666 MHz",
			"capacity-byte": 1073741824,
			"human_readable_capacity": "1024 MB",
			"ram-type": "ddr2",
			"ram-ecc": "yes",
			"ram-timings": "5-5-5-15"
		}
	]
	output = read_decode_dimms.read_decode_dimms(filedir + 'dimms.txt')

	assert output == expect


def test_baseboard():
	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P5VD2-VM",
		"sn": "123456789000",
	}
	output = read_dmidecode.get_baseboard(filedir + 'baseboard.txt')

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASUSTeK Computer INC.",
		"model": "P5VD2-VM",
		"sn": "123456789000",
		"serial-ports-n": 1,
		"parallel-ports-n": 1,
		"usb-ports-n": 8,
		"ps2-ports-n": 2,
		"sata-ports-n": 3,
		"esata-ports-n": 1,
		"vga-ports-n": 1,
		"ethernet-ports-n": 1,
		"mini-jack-ports-n": 3,
		"ide-ports-n": 2,
		"notes": "Unknown connector: None / None (SPDIF_OUT / SPDIF_OUT)"
	}
	output = read_dmidecode.get_connectors(filedir + 'connector.txt', baseboard)

	assert output == expect


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Chassis Manufacture",
		"model": "",
		"sn": "EVAL",
		"motherboard-form-factor": ""
	}
	output = read_dmidecode.get_chassis(filedir + 'chassis.txt')

	assert output == expect


def test_smartctl():
	expect = [
		{
			"type": "hdd",
			"brand": "Maxtor",
			"model": "6Y080L0",
			"family": "DiamondMax Plus 9",
			"wwn": "",
			"sn": "Y2E5CRAE",
			"capacity-decibyte": 82000000000,
			"human_readable_capacity": "81,9 GB",
			"spin-rate-rpm": -1,
			"smart-data": "ok",
			'notes': "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  3 Spin_Up_Time            POS--K   194   157   063    -    21293\n  4 Start_Stop_Count        -O--CK   253   253   000    -    1539\n  5 Reallocated_Sector_Ct   PO--CK   253   253   063    -    3\n  6 Read_Channel_Margin     P-----   253   253   100    -    0\n  7 Seek_Error_Rate         -O-R--   253   252   000    -    0\n  8 Seek_Time_Performance   POS--K   253   244   187    -    44709\n  9 Power_On_Minutes        -O--CK   124   124   000    -    1009h+15m\n 10 Spin_Retry_Count        PO-R-K   251   232   157    -    2\n 11 Calibration_Retry_Count PO-R-K   253   252   223    -    0\n 12 Power_Cycle_Count       -O--CK   251   251   000    -    1169\n192 Power-Off_Retract_Count -O--CK   253   253   000    -    0\n193 Load_Cycle_Count        -O--CK   253   253   000    -    0\n194 Temperature_Celsius     -O--CK   253   253   000    -    36\n195 Hardware_ECC_Recovered  -O-R--   253   252   000    -    614\n196 Reallocated_Event_Count ---R--   250   250   000    -    3\n197 Current_Pending_Sector  ---R--   253   253   000    -    0\n198 Offline_Uncorrectable   ---R--   153   153   000    -    100\n199 UDMA_CRC_Error_Count    ---R--   198   196   000    -    3\n200 Multi_Zone_Error_Rate   -O-R--   253   252   000    -    0\n201 Soft_Read_Error_Rate    -O-R--   253   236   000    -    186\n202 Data_Address_Mark_Errs  -O-R--   253   251   000    -    0\n203 Run_Out_Cancel          PO-R--   253   252   180    -    11\n204 Soft_ECC_Correction     -O-R--   253   252   000    -    0\n205 Thermal_Asperity_Rate   -O-R--   253   252   000    -    0\n207 Spin_High_Current       -O-R-K   251   232   000    -    2\n208 Spin_Buzz               -O-R-K   253   252   000    -    0\n209 Offline_Seek_Performnce --S--K   201   200   000    -    0\n 99 Unknown_Attribute       --S---   253   253   000    -    0\n100 Unknown_Attribute       --S---   253   253   000    -    0\n101 Unknown_Attribute       --S---   253   253   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning"
		}
	]
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
