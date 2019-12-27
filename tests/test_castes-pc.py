#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = 'castes-pc/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "ZOTAC International (MCO) Ltd.",
		"model": "GeForce GTX 1060 6GB",
		'internal-name': 'GP106',
		"capacity-byte": 6442450944,
		"human_readable_capacity": "6144 MB",
		"brand-manufacturer": "Nvidia"
	}
	output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(True, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert output == expect


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-64",
		"model": "Core i5-6500",
		"brand": "Intel",
		"core-n": 4,
		"thread-n": 4,
		"frequency-hertz": 3200000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu.read_lscpu(filedir + 'lscpu.txt')

	assert output == expect


def test_ram():
	expect = [
		{
			"type": "ram",
			"working": "yes",
			"brand": "Synertek",
			"model": "Undefined",
			"sn": "",
			"frequency-hertz": -1,
			"human_readable_frequency": "",
			"capacity-byte": -1,
			"human_readable_capacity": "",
			"ram-type": "",
			"ram-ecc": "no",
			"ram-timings": ""
		},
		{
			"type": "ram",
			"working": "yes",
			"brand": "Synertek",
			"model": "Undefined",
			"sn": "",
			"frequency-hertz": -1,
			"human_readable_frequency": "",
			"capacity-byte": -1,
			"human_readable_capacity": "",
			"ram-type": "",
			"ram-ecc": "no",
			"ram-timings": ""
		}
	]
	output = read_decode_dimms.read_decode_dimms(filedir + 'dimms.txt')

	assert len(output) == 2, "2 RAM modules are found"
	assert output == expect


def test_baseboard():
	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASRock",
		"model": "H110M-ITX/ac",
		"sn": "M80-69017400518",
	}
	output = read_dmidecode.get_baseboard(filedir + 'baseboard.txt')

	assert output == expect


def test_connector():
	baseboard = read_dmidecode.get_baseboard(filedir + 'baseboard.txt')

	# This is entirely wrong and is not reflected by any means from reality and the real motherboard, but the manufacturer
	# dropped all this garbage into the DMI information, so here we go...
	expect = {
		"type": "motherboard",
		"working": "yes",
		"brand": "ASRock",
		"model": "H110M-ITX/ac",
		"sn": "M80-69017400518",
		"notes": ""
	}
	output = read_dmidecode.get_connectors(filedir + 'connector.txt', baseboard)

	assert output == expect


def test_chassis():
	# This is also wrong, but for pre-assembled computers it should be right
	expect = {
		"type": "case",
		"brand": "To Be Filled By O.E.M.",
		"model": "",
		"sn": "To Be Filled By O.E.M.",
		"motherboard-form-factor": ""
	}
	output = read_dmidecode.get_chassis(filedir + 'chassis.txt')

	assert output == expect


def test_smartctl():
	expect = [
		{
			"type": "ssd",
			"brand": "",
			"model": "DREVO X1 SSD",
			"family": "",
			"hdd-form-factor": "2.5-7mm",
			"sn": "TX1711901797",
			'wwn': '0 000000 000000000',  # Nice
			"capacity-byte": 240000000000,
			"human_readable_capacity": "240 GB",
			"smart-data": "ok",
			'sata-ports-n': 1,
			'notes': "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     -O--CK   100   100   050    -    0\n  5 Reallocated_Sector_Ct   -O--CK   100   100   050    -    52\n  9 Power_On_Hours          -O--CK   100   100   050    -    1668\n 12 Power_Cycle_Count       -O--CK   100   100   050    -    829\n160 Unknown_Attribute       -O--CK   100   100   050    -    19\n161 Unknown_Attribute       PO--CK   100   100   050    -    35\n163 Unknown_Attribute       -O--CK   100   100   050    -    15\n164 Unknown_Attribute       -O--CK   100   100   050    -    42113\n165 Unknown_Attribute       -O--CK   100   100   050    -    114\n166 Unknown_Attribute       -O--CK   100   100   050    -    10\n167 Unknown_Attribute       -O--CK   100   100   050    -    79\n168 Unknown_Attribute       -O--CK   100   100   050    -    3000\n169 Unknown_Attribute       -O--CK   100   100   050    -    98\n175 Program_Fail_Count_Chip -O--CK   100   100   050    -    0\n176 Erase_Fail_Count_Chip   -O--CK   100   100   050    -    0\n177 Wear_Leveling_Count     -O--CK   100   100   050    -    0\n178 Used_Rsvd_Blk_Cnt_Chip  -O--CK   100   100   050    -    52\n181 Program_Fail_Cnt_Total  -O--CK   100   100   050    -    0\n182 Erase_Fail_Count_Total  -O--CK   100   100   050    -    0\n192 Power-Off_Retract_Count -O--CK   100   100   050    -    68\n194 Temperature_Celsius     -O---K   100   100   050    -    38\n195 Hardware_ECC_Recovered  -O--CK   100   100   050    -    92762\n196 Reallocated_Event_Count -O--CK   100   100   050    -    19\n197 Current_Pending_Sector  -O--CK   100   100   050    -    52\n198 Offline_Uncorrectable   -O--CK   100   100   050    -    19\n199 UDMA_CRC_Error_Count    -O--CK   100   100   050    -    0\n232 Available_Reservd_Space -O--CK   100   100   050    -    35\n241 Total_LBAs_Written      ----CK   100   100   050    -    147066\n242 Total_LBAs_Read         ----CK   100   100   050    -    238128\n245 Unknown_Attribute       -O--CK   100   100   050    -    242467\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning"
		},
		{
			"type": "hdd",
			"brand": "Seagate",
			"model": "ST9750420AS",
			"family": "Momentus 7200.5",
			"wwn": "5 000c50 0614757a2",
			"sn": "6WS3155L",
			"capacity-decibyte": 750000000000,
			"human_readable_capacity": "750 GB",
			"spin-rate-rpm": 7200,
			"smart-data": "ok",
			'sata-ports-n': 1,
			'notes': "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR--   119   099   006    -    206410160\n  3 Spin_Up_Time            PO----   098   097   085    -    0\n  4 Start_Stop_Count        -O--CK   099   099   020    -    1940\n  5 Reallocated_Sector_Ct   PO--CK   100   100   036    -    0\n  7 Seek_Error_Rate         POSR--   074   060   030    -    27414184\n  9 Power_On_Hours          -O--CK   098   098   000    -    2017\n 10 Spin_Retry_Count        PO--C-   100   100   097    -    0\n 12 Power_Cycle_Count       -O--CK   100   100   020    -    966\n184 End-to-End_Error        -O--CK   100   100   099    -    0\n187 Reported_Uncorrect      -O--CK   100   100   000    -    0\n188 Command_Timeout         -O--CK   100   100   000    -    1\n189 High_Fly_Writes         -O-RCK   100   100   000    -    0\n190 Airflow_Temperature_Cel -O---K   071   043   045    Past 29 (0 2 29 24 0)\n191 G-Sense_Error_Rate      -O--CK   100   100   000    -    11\n192 Power-Off_Retract_Count -O--CK   100   100   000    -    164\n193 Load_Cycle_Count        -O--CK   018   018   000    -    164806\n194 Temperature_Celsius     -O---K   029   057   000    -    29 (0 19 0 0 0)\n195 Hardware_ECC_Recovered  -O-RC-   119   099   000    -    206410160\n197 Current_Pending_Sector  -O--C-   100   100   000    -    0\n198 Offline_Uncorrectable   ----C-   100   100   000    -    0\n199 UDMA_CRC_Error_Count    -OSRCK   200   200   000    -    0\n240 Head_Flying_Hours       ------   100   253   000    -    1103 (11 165 0)\n241 Total_LBAs_Written      ------   100   253   000    -    2988175193\n242 Total_LBAs_Read         ------   100   253   000    -    711974475\n254 Free_Fall_Sensor        -O--CK   100   100   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning"
		}
	]
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
