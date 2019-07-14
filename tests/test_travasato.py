#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'travasato/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"brand": "ASUSTeK Computer Inc.",
		"model": "GeForce GT 610",
		"internal-name": "GF119",
		"capacity-byte": None,  # Still no glxinfo :(
		"human_readable_capacity": "",
		"brand-manufacturer": "Nvidia"
	}
	output = read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"isa": "x86-64",
		"model": "Core 2 Quad Q6600",
		"brand": "Intel",
		"core-n": 4,
		"thread-n": 4,
		"frequency-hertz": 2400000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu(filedir + 'lscpu.txt')

	assert expect == output


def test_ram():
	expect = [
		{
			"type": "ram",
			"brand": "Kingston",
			"model": "K",
			"sn": "3375612238",
			"frequency-hertz": 666000000,
			"human_readable_frequency": "666 MHz",
			"capacity-byte": 2147483648,
			"human_readable_capacity": "2048 MB",
			"ram-type": "ddr2",
			"ram-ecc": "yes",
			"ram-timings": "5-5-5-15"
		},
		{
			"type": "ram",
			"brand": "Kingston",
			"model": "K",
			"sn": "3392385358",
			"frequency-hertz": 666000000,
			"human_readable_frequency": "666 MHz",
			"capacity-byte": 2147483648,
			"human_readable_capacity": "2048 MB",
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
		"brand": "Intel Corporation",
		"model": "D975XBX2",
		"sn": "BAOB4B9001YY",
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
		"brand": "Intel Corporation",
		"model": "D975XBX2",
		"sn": "BAOB4B9001YY",
		"ide-ports-n": 2,
		"notes": ""
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	# At least it's not assuming stuff it cannot know...
	expect = {
		"type": "case",
		"brand": "",
		"model": "",
		"sn": "",
		"motherboard-form-factor": ""
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


def test_smartctl():
	expect = [
		{
			"type": "hdd",
			"brand": "Hitachi",
			"model": "HDT725025VLA380",
			"family": "Deskstar T7K500",
			"wwn": "5 000cca 6904de32c",
			"sn": "VFA100R24D8ELK",
			"capacity-decibyte": 250000000000,
			"human_readable_capacity": "250 GB",
			"spin-rate-rpm": -1,
			"human_readable_smart_data": "=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x00)\tOffline data collection activity\n\t\t\t\t\twas never started.\n\t\t\t\t\tAuto Offline Data Collection: Disabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t( 4949) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x5b) SMART execute Offline immediate.\n\t\t\t\t\tAuto Offline data collection on/off support.\n\t\t\t\t\tSuspend Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tOffline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tNo Conveyance Self-test supported.\n\t\t\t\t\tSelective Self-test supported.\nSMART capabilities:            (0x0003)\tSaves SMART data before entering\n\t\t\t\t\tpower-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tGeneral Purpose Logging supported.\nShort self-test routine \nrecommended polling time: \t (   1) minutes.\nExtended self-test routine\nrecommended polling time: \t (  83) minutes.\nSCT capabilities: \t       (0x003f)\tSCT Status supported.\n\t\t\t\t\tSCT Error Recovery Control supported.\n\t\t\t\t\tSCT Feature Control supported.\n\t\t\t\t\tSCT Data Table supported.\n\nSMART Attributes Data Structure revision number: 16\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     PO-R--   100   100   016    -    0\n  2 Throughput_Performance  P-S---   100   100   050    -    0\n  3 Spin_Up_Time            POS---   115   115   024    -    330 (Average 321)\n  4 Start_Stop_Count        -O--C-   100   100   000    -    89\n  5 Reallocated_Sector_Ct   PO--CK   100   100   005    -    4\n  7 Seek_Error_Rate         PO-R--   100   100   067    -    0\n  8 Seek_Time_Performance   P-S---   100   100   020    -    0\n  9 Power_On_Hours          -O--C-   090   090   000    -    74780\n 10 Spin_Retry_Count        PO--C-   100   100   060    -    0\n 12 Power_Cycle_Count       -O--CK   100   100   000    -    89\n192 Power-Off_Retract_Count -O--CK   098   098   000    -    3201\n193 Load_Cycle_Count        -O--C-   098   098   000    -    3201\n194 Temperature_Celsius     -O----   176   176   000    -    34 (Min/Max 14/56)\n196 Reallocated_Event_Count -O--CK   100   100   000    -    4\n197 Current_Pending_Sector  -O---K   100   100   000    -    0\n198 Offline_Uncorrectable   ---R--   100   100   000    -    0\n199 UDMA_CRC_Error_Count    -O-R--   200   253   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nGeneral Purpose Log Directory Version 1\nSMART           Log Directory Version 1 [multi-sector log support]\nAddress    Access  R/W   Size  Description\n0x00       GPL,SL  R/O      1  Log Directory\n0x01           SL  R/O      1  Summary SMART error log\n0x03       GPL     R/O      1  Ext. Comprehensive SMART error log\n0x06           SL  R/O      1  SMART self-test log\n0x07       GPL     R/O      1  Extended self-test log\n0x09           SL  R/W      1  Selective self-test log\n0x10       GPL     R/O      1  SATA NCQ Queued Error log\n0x11       GPL     R/O      1  SATA Phy Event Counters log\n0x20       GPL     R/O      1  Streaming performance log [OBS-8]\n0x21       GPL     R/O      1  Write stream error log\n0x22       GPL     R/O      1  Read stream error log\n0x80-0x9f  GPL,SL  R/W     16  Host vendor specific log\n0xe0       GPL,SL  R/W      1  SCT Command/Status\n0xe1       GPL,SL  R/W      1  SCT Data Transfer\n\nSMART Extended Comprehensive Error Log Version: 1 (1 sectors)\nDevice Error Count: 1\n\tCR     = Command Register\n\tFEATR  = Features Register\n\tCOUNT  = Count (was: Sector Count) Register\n\tLBA_48 = Upper bytes of LBA High/Mid/Low Registers ]  ATA-8\n\tLH     = LBA High (was: Cylinder High) Register    ]   LBA\n\tLM     = LBA Mid (was: Cylinder Low) Register      ] Register\n\tLL     = LBA Low (was: Sector Number) Register     ]\n\tDV     = Device (was: Device/Head) Register\n\tDC     = Device Control Register\n\tER     = Error register\n\tST     = Status register\nPowered_Up_Time is measured from power on, and printed as\nDDd+hh:mm:SS.sss where DD=days, hh=hours, mm=minutes,\nSS=sec, and sss=millisec. It \"wraps\" after 49.710 days.\n\nError 1 [0] occurred at disk power-on lifetime: 2606 hours (108 days + 14 hours)\n  When the command that caused the error occurred, the device was active or idle.\n\n  After command completion occurred, registers were:\n  ER -- ST COUNT  LBA_48  LH LM LL DV DC\n  -- -- -- == -- == == == -- -- -- -- --\n  40 -- 51 00 06 00 00 12 8a ad 7a e2 00  Error: UNC 6 sectors at LBA = 0x128aad7a = 311078266\n\n  Commands leading to the command that caused the error were:\n  CR FEATR COUNT  LBA_48  LH LM LL DV DC  Powered_Up_Time  Command/Feature_Name\n  -- == -- == -- == == == -- -- -- -- --  ---------------  --------------------\n  25 00 00 00 40 00 00 12 8a ad 40 e0 00     01:28:28.800  READ DMA EXT\n  25 00 00 00 40 00 00 12 8a ad 00 e0 00     01:28:28.800  READ DMA EXT\n  25 00 00 00 40 00 00 12 8a ac c0 e0 00     01:28:28.800  READ DMA EXT\n  25 00 00 00 40 00 00 12 8a ac 80 e0 00     01:28:28.800  READ DMA EXT\n  25 00 00 00 40 00 00 12 8a ac 40 e0 00     01:28:28.800  READ DMA EXT\n\nSMART Extended Self-test Log Version: 1 (1 sectors)\nNo self-tests have been logged.  [To run self-tests, use: smartctl -t]\n\nSMART Selective self-test log data structure revision number 1\n SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS\n    1        0        0  Not_testing\n    2        0        0  Not_testing\n    3        0        0  Not_testing\n    4        0        0  Not_testing\n    5        0        0  Not_testing\nSelective self-test flags (0x0):\n  After scanning selected spans, do NOT read-scan remainder of disk.\nIf Selective self-test is pending on power-up, resume after 0 minute delay.\n\nSCT Status Version:                  2\nSCT Version (vendor specific):       256 (0x0100)\nSCT Support Level:                   1\nDevice State:                        Active (0)\nCurrent Temperature:                 34 Celsius\nPower Cycle Max Temperature:         39 Celsius\nLifetime    Max Temperature:         56 Celsius\n\nSCT Temperature History Version:     2\nTemperature Sampling Period:         1 minute\nTemperature Logging Interval:        1 minute\nMin/Max recommended Temperature:      5/60 Celsius\nMin/Max Temperature Limit:           -40/65 Celsius\nTemperature History Size (Index):    128 (19)\n\nIndex    Estimated Time   Temperature Celsius\n  20    2019-04-16 07:13    33  **************\n ...    ..(116 skipped).    ..  **************\n   9    2019-04-16 09:10    33  **************\n  10    2019-04-16 09:11    34  ***************\n  11    2019-04-16 09:12    33  **************\n  12    2019-04-16 09:13    33  **************\n  13    2019-04-16 09:14    34  ***************\n ...    ..(  2 skipped).    ..  ***************\n  16    2019-04-16 09:17    34  ***************\n  17    2019-04-16 09:18    33  **************\n  18    2019-04-16 09:19    33  **************\n  19    2019-04-16 09:20    33  **************\n\nSCT Error Recovery Control:\n           Read: Disabled\n          Write: Disabled\n\nDevice Statistics (GP/SMART Log 0x04) not supported\n\nSATA Phy Event Counters (GP Log 0x11)\nID      Size     Value  Description\n0x0001  2            0  Command failed due to ICRC error\n0x0009  2            6  Transition from drive PhyRdy to drive PhyNRdy\n0x000a  2            5  Device-to-host register FISes sent due to a COMRESET\n0x000b  2            0  CRC errors within host-to-device FIS\n0x000d  2            0  Non-CRC errors within host-to-device FIS\n\n"
		}
	]
	output = read_smartctl(filedir)

	assert expect == output
