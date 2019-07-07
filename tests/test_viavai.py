#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'viavai/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"brand": "ASUSTeK Computer Inc.",
		"model": "Chrome 9 HC",
		"internal-name": "CN896/VN896/P4M900",
		"capacity-byte": None,
		"human_readable_capacity": "",
		"brand-manufacturer": "VIA"
	}
	output = read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"architecture": "x86-64",
		"model": "Celeron 2.80GHz",
		"brand": "Intel",
		"core-n": 1,
		"thread-n": 1,
		"frequency-hertz": 2800000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu(filedir + 'lscpu.txt')

	assert expect == output


def test_ram():
	expect = [
		{
			"type": "ram",
			"brand": "Kingston",
			"model": "KD6502-ELG",
			"sn": "3072778780",
			"frequency-hertz": 666000000,
			"human_readable_frequency": "666 MHz",
			"capacity-byte": 1073741824,
			"human_readable_capacity": "1024 MB",
			"ram-type": "ddr2",
			"ram-ecc": "yes",
			"ram-timings": "5-5-5-15"
		}
	]
	output = read_decode_dimms(filedir + 'dimms.txt')

	assert expect == output


def test_baseboard():
	expect = {
		"type": "motherboard",
		"brand": "ASUSTeK Computer INC.",
		"model": "P5VD2-VM",
		"sn": "123456789000",
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
		"brand": "ASUSTeK Computer INC.",
		"model": "P5VD2-VM",
		"sn": "123456789000",
		"serial-ports-n": 1,
		"parallel-ports-n": 1,
		"usb-ports-n": 8,
		"ps2-ports-n": 2,
		"sata-ports-n": 3,
		"vga-ports-n": 1,
		"ethernet-ports-n": 1,
		"mini-jack-ports-n": 3,
		"ide-ports-n": 2,
		"notes": "Unknown connector: None / None (SPDIF_OUT / SPDIF_OUT)\nUnknown connector: On Board IDE / None (ESATA / Not Specified)"
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Chassis Manufacture",
		"model": "",
		"sn": "EVAL",
		"motherboard-form-factor": ""
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


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
			"smart-data": "=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x82)\tOffline data collection activity\n\t\t\t\t\twas completed without error.\n\t\t\t\t\tAuto Offline Data Collection: Enabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t(  242) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x5b) SMART execute Offline immediate.\n\t\t\t\t\tAuto Offline data collection on/off support.\n\t\t\t\t\tSuspend Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tOffline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tNo Conveyance Self-test supported.\n\t\t\t\t\tSelective Self-test supported.\nSMART capabilities:            (0x0003)\tSaves SMART data before entering\n\t\t\t\t\tpower-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tNo General Purpose Logging support.\nShort self-test routine \nrecommended polling time: \t (   2) minutes.\nExtended self-test routine\nrecommended polling time: \t (  41) minutes.\n\nSMART Attributes Data Structure revision number: 16\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  3 Spin_Up_Time            POS--K   194   157   063    -    21293\n  4 Start_Stop_Count        -O--CK   253   253   000    -    1539\n  5 Reallocated_Sector_Ct   PO--CK   253   253   063    -    3\n  6 Read_Channel_Margin     P-----   253   253   100    -    0\n  7 Seek_Error_Rate         -O-R--   253   252   000    -    0\n  8 Seek_Time_Performance   POS--K   253   244   187    -    44709\n  9 Power_On_Minutes        -O--CK   124   124   000    -    1009h+15m\n 10 Spin_Retry_Count        PO-R-K   251   232   157    -    2\n 11 Calibration_Retry_Count PO-R-K   253   252   223    -    0\n 12 Power_Cycle_Count       -O--CK   251   251   000    -    1169\n192 Power-Off_Retract_Count -O--CK   253   253   000    -    0\n193 Load_Cycle_Count        -O--CK   253   253   000    -    0\n194 Temperature_Celsius     -O--CK   253   253   000    -    36\n195 Hardware_ECC_Recovered  -O-R--   253   252   000    -    614\n196 Reallocated_Event_Count ---R--   250   250   000    -    3\n197 Current_Pending_Sector  ---R--   253   253   000    -    0\n198 Offline_Uncorrectable   ---R--   153   153   000    -    100\n199 UDMA_CRC_Error_Count    ---R--   198   196   000    -    3\n200 Multi_Zone_Error_Rate   -O-R--   253   252   000    -    0\n201 Soft_Read_Error_Rate    -O-R--   253   236   000    -    186\n202 Data_Address_Mark_Errs  -O-R--   253   251   000    -    0\n203 Run_Out_Cancel          PO-R--   253   252   180    -    11\n204 Soft_ECC_Correction     -O-R--   253   252   000    -    0\n205 Thermal_Asperity_Rate   -O-R--   253   252   000    -    0\n207 Spin_High_Current       -O-R-K   251   232   000    -    2\n208 Spin_Buzz               -O-R-K   253   252   000    -    0\n209 Offline_Seek_Performnce --S--K   201   200   000    -    0\n 99 Unknown_Attribute       --S---   253   253   000    -    0\n100 Unknown_Attribute       --S---   253   253   000    -    0\n101 Unknown_Attribute       --S---   253   253   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nRead SMART Log Directory failed: scsi error badly formed scsi parameters\n\nGeneral Purpose Log Directory not supported\n\nSMART Extended Comprehensive Error Log (GP Log 0x03) not supported\n\nSMART Error Log Version: 1\nATA Error Count: 20 (device log contains only the most recent five errors)\n\tCR = Command Register [HEX]\n\tFR = Features Register [HEX]\n\tSC = Sector Count Register [HEX]\n\tSN = Sector Number Register [HEX]\n\tCL = Cylinder Low Register [HEX]\n\tCH = Cylinder High Register [HEX]\n\tDH = Device/Head Register [HEX]\n\tDC = Device Command Register [HEX]\n\tER = Error register [HEX]\n\tST = Status register [HEX]\nPowered_Up_Time is measured from power on, and printed as\nDDd+hh:mm:SS.sss where DD=days, hh=hours, mm=minutes,\nSS=sec, and sss=millisec. It \"wraps\" after 49.710 days.\n\nError 20 occurred at disk power-on lifetime: 32585 hours (1357 days + 17 hours)\n  When the command that caused the error occurred, the device was in an unknown state.\n\n  After command completion occurred, registers were:\n  ER ST SC SN CL CH DH\n  -- -- -- -- -- -- --\n  84 51 00 07 e1 5b e1  Error: ICRC, ABRT at LBA = 0x015be107 = 22798599\n\n  Commands leading to the command that caused the error were:\n  CR FR SC SN CL CH DH DC   Powered_Up_Time  Command/Feature_Name\n  -- -- -- -- -- -- -- --  ----------------  --------------------\n  c8 00 38 07 e1 5b e1 00  17d+06:12:01.552  READ DMA\n  c8 00 50 0f 9f 59 e1 00  17d+06:12:01.536  READ DMA\n  c8 00 08 df 5e 00 e0 00  17d+06:12:01.536  READ DMA\n  c8 00 58 4f 47 74 e2 00  17d+06:12:01.536  READ DMA\n  c8 00 38 7f af 5d e1 00  17d+06:12:01.536  READ DMA\n\nError 19 occurred at disk power-on lifetime: 21739 hours (905 days + 19 hours)\n  When the command that caused the error occurred, the device was in an unknown state.\n\n  After command completion occurred, registers were:\n  ER ST SC SN CL CH DH\n  -- -- -- -- -- -- --\n  40 51 01 7c 4b 67 e1  Error: UNC at LBA = 0x01674b7c = 23546748\n\n  Commands leading to the command that caused the error were:\n  CR FR SC SN CL CH DH DC   Powered_Up_Time  Command/Feature_Name\n  -- -- -- -- -- -- -- --  ----------------  --------------------\n  40 00 01 7c 4b 67 e1 00      02:21:45.328  READ VERIFY SECTOR(S)\n  40 00 01 7b 4b 67 e1 00      02:21:44.304  READ VERIFY SECTOR(S)\n  40 00 01 7a 4b 67 e1 00      02:21:43.376  READ VERIFY SECTOR(S)\n  40 00 01 79 4b 67 e1 00      02:21:43.360  READ VERIFY SECTOR(S)\n  40 00 02 7d 4b 67 e1 00      02:21:42.416  READ VERIFY SECTOR(S)\n\nError 18 occurred at disk power-on lifetime: 21739 hours (905 days + 19 hours)\n  When the command that caused the error occurred, the device was in an unknown state.\n\n  After command completion occurred, registers were:\n  ER ST SC SN CL CH DH\n  -- -- -- -- -- -- --\n  40 51 01 7b 4b 67 e1  Error: UNC at LBA = 0x01674b7b = 23546747\n\n  Commands leading to the command that caused the error were:\n  CR FR SC SN CL CH DH DC   Powered_Up_Time  Command/Feature_Name\n  -- -- -- -- -- -- -- --  ----------------  --------------------\n  40 00 01 7b 4b 67 e1 00      02:21:44.304  READ VERIFY SECTOR(S)\n  40 00 01 7a 4b 67 e1 00      02:21:43.376  READ VERIFY SECTOR(S)\n  40 00 01 79 4b 67 e1 00      02:21:43.360  READ VERIFY SECTOR(S)\n  40 00 02 7d 4b 67 e1 00      02:21:42.416  READ VERIFY SECTOR(S)\n  40 00 02 7b 4b 67 e1 00      02:21:41.392  READ VERIFY SECTOR(S)\n\nError 17 occurred at disk power-on lifetime: 21739 hours (905 days + 19 hours)\n  When the command that caused the error occurred, the device was in an unknown state.\n\n  After command completion occurred, registers were:\n  ER ST SC SN CL CH DH\n  -- -- -- -- -- -- --\n  40 51 01 7a 4b 67 e1  Error: UNC at LBA = 0x01674b7a = 23546746\n\n  Commands leading to the command that caused the error were:\n  CR FR SC SN CL CH DH DC   Powered_Up_Time  Command/Feature_Name\n  -- -- -- -- -- -- -- --  ----------------  --------------------\n  40 00 01 7a 4b 67 e1 00      02:21:43.376  READ VERIFY SECTOR(S)\n  40 00 01 79 4b 67 e1 00      02:21:43.360  READ VERIFY SECTOR(S)\n  40 00 02 7d 4b 67 e1 00      02:21:42.416  READ VERIFY SECTOR(S)\n  40 00 02 7b 4b 67 e1 00      02:21:41.392  READ VERIFY SECTOR(S)\n  40 00 02 79 4b 67 e1 00      02:21:40.528  READ VERIFY SECTOR(S)\n\nError 16 occurred at disk power-on lifetime: 21739 hours (905 days + 19 hours)\n  When the command that caused the error occurred, the device was in an unknown state.\n\n  After command completion occurred, registers were:\n  ER ST SC SN CL CH DH\n  -- -- -- -- -- -- --\n  40 51 02 7d 4b 67 e1  Error: UNC at LBA = 0x01674b7d = 23546749\n\n  Commands leading to the command that caused the error were:\n  CR FR SC SN CL CH DH DC   Powered_Up_Time  Command/Feature_Name\n  -- -- -- -- -- -- -- --  ----------------  --------------------\n  40 00 02 7d 4b 67 e1 00      02:21:42.416  READ VERIFY SECTOR(S)\n  40 00 02 7b 4b 67 e1 00      02:21:41.392  READ VERIFY SECTOR(S)\n  40 00 02 79 4b 67 e1 00      02:21:40.528  READ VERIFY SECTOR(S)\n  40 00 02 77 4b 67 e1 00      02:21:40.528  READ VERIFY SECTOR(S)\n  40 00 04 7b 4b 67 e1 00      02:21:39.504  READ VERIFY SECTOR(S)\n\nSMART Extended Self-test Log (GP Log 0x07) not supported\n\nSMART Self-test log structure revision number 1\nNo self-tests have been logged.  [To run self-tests, use: smartctl -t]\n\nSMART Selective self-test log data structure revision number 1\n SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS\n    1        0        0  Not_testing\n    2        0        0  Not_testing\n    3        0        0  Not_testing\n    4        0        0  Not_testing\n    5        0        0  Not_testing\nSelective self-test flags (0x0):\n  After scanning selected spans, do NOT read-scan remainder of disk.\nIf Selective self-test is pending on power-up, resume after 0 minute delay.\n\nSCT Commands not supported\n\nDevice Statistics (GP/SMART Log 0x04) not supported\n\nSATA Phy Event Counters (GP Log 0x11) not supported\n\n"
		}
	]
	output = read_smartctl(filedir)

	assert expect == output
