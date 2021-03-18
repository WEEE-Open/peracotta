#!/usr/bin/env python3

from parsers import read_smartctl

filedir = 'tests/hdd/'


def test_smartctl():
	expect = [
		{
			"type": "hdd",
			"brand": "Toshiba",
			"model": "MQ01ABF050",
			"family": "2.5\" HDD MQ01ABF...",
			"sn": "76H3EUCL",
			"sata-ports-n": 1,
			"wwn": "5 000039 7222954ce",
			'capacity-decibyte': 500000000000,
			'spin-rate-rpm': 5400,
			'smart-data': 'ok',
			'hdd-form-factor': '2.5-7mm',
			'notes': "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     PO-R--   100   100   050    -    0\n  2 Throughput_Performance  P-S---   100   100   050    -    0\n  3 Spin_Up_Time            POS--K   100   100   001    -    1268\n  4 Start_Stop_Count        -O--CK   100   100   000    -    9310\n  5 Reallocated_Sector_Ct   PO--CK   100   100   050    -    0\n  7 Seek_Error_Rate         PO-R--   100   100   050    -    0\n  8 Seek_Time_Performance   P-S---   100   100   050    -    0\n  9 Power_On_Hours          -O--CK   091   091   000    -    3990\n 10 Spin_Retry_Count        PO--CK   253   100   030    -    0\n 12 Power_Cycle_Count       -O--CK   100   100   000    -    3178\n191 G-Sense_Error_Rate      -O--CK   100   100   000    -    1501\n192 Power-Off_Retract_Count -O--CK   100   100   000    -    62\n193 Load_Cycle_Count        -O--CK   086   086   000    -    148398\n194 Temperature_Celsius     -O---K   100   100   000    -    28 (Min/Max 13/44)\n196 Reallocated_Event_Count -O--CK   100   100   000    -    0\n197 Current_Pending_Sector  -O--CK   100   100   000    -    0\n198 Offline_Uncorrectable   ----CK   100   100   000    -    0\n199 UDMA_CRC_Error_Count    -O--CK   200   200   000    -    2945\n220 Disk_Shift              -O----   100   100   000    -    0\n222 Loaded_Hours            -O--CK   092   092   000    -    3421\n223 Load_Retry_Count        -O--CK   100   100   000    -    0\n224 Load_Friction           -O---K   100   100   000    -    0\n226 Load-in_Time            -OS--K   100   100   000    -    197\n240 Head_Flying_Hours       P-----   100   100   001    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning"
		}

	]
	output = read_smartctl.read_smartctl(filedir)

	assert output == expect
