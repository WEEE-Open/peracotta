#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo

filedir = '2014-castes-mbp/'


def test_lspci():
	expect = {
		'type': 'graphics-card',
		'brand-manufacturer': 'Nvidia',
		'brand': 'Apple Inc. GK107M',
		'model': 'GeForce GT 750M Mac Edition',
		'capacity-byte': 2147483648,
		'human_readable_capacity': '2048 MB'
	}
	output = read_lspci_and_glxinfo(True, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_ram():
	output = read_decode_dimms(filedir + 'dimms.txt')

	assert len(output) == 0


def test_baseboard():
	expect = {
		'type': 'motherboard',
		'brand': 'Apple Inc.',
		'model': 'Mac-2BD1B31983FE1663',
		'sn': '***REMOVED***'
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		'type': 'motherboard',
		'brand': 'Apple Inc.',
		'model': 'Mac-2BD1B31983FE1663',
		'sn': '***REMOVED***',
		'usb-ports-n': 3,
		'mini-jack-ports-n': 1,
		'hdmi-ports-n': 1,
		'mini-displayport-ports-n': 2,
		'power-connector': 'proprietary',
		'warning': ''
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	expect = {
		'brand': 'Apple Inc.',
		'sn': 'CENSORED',
		'type': 'case',
		'motherboard-form-factor': 'proprietary-laptop',
		'model': '',
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


def test_smartctl():
	expect = [
		{
			'type': 'ssd',
			'brand': 'Apple SD/SM/TS...E/F/G SSDs',
			'model': 'APPLE SSD SM0512F',
			'sn': '***REMOVED***',
			'family': '',
			'capacity-byte': 500000000000,
			'human_readable_capacity': '500 GB',
			'smart-data': '=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x00)\tOffline data collection activity\n\t\t\t\t\twas never started.\n\t\t\t\t\tAuto Offline Data Collection: Disabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t(    0) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x5f) SMART execute Offline immediate.\n\t\t\t\t\tAuto Offline data collection on/off support.\n\t\t\t\t\tAbort Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tOffline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tNo Conveyance Self-test supported.\n\t\t\t\t\tSelective Self-test supported.\nSMART capabilities:            (0x0003)\tSaves SMART data before entering\n\t\t\t\t\tpower-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tGeneral Purpose Logging supported.\nShort self-test routine \nrecommended polling time: \t (   2) minutes.\nExtended self-test routine\nrecommended polling time: \t (  10) minutes.\n\nSMART Attributes Data Structure revision number: 40\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     -O-RC-   200   200   000    -    0\n  5 Reallocated_Sector_Ct   PO--CK   100   100   000    -    0\n  9 Power_On_Hours          -O--CK   097   097   000    -    10399\n 12 Power_Cycle_Count       -O--CK   087   087   000    -    12802\n169 Unknown_Apple_Attrib    PO--C-   253   253   010    -    3312107658752\n173 Wear_Leveling_Count     -O--CK   186   186   100    -    584144191767\n174 Host_Reads_MiB          -O---K   099   099   000    -    49185503\n175 Host_Writes_MiB         -O---K   099   099   000    -    39494747\n192 Power-Off_Retract_Count -O--C-   099   099   000    -    254\n194 Temperature_Celsius     -O---K   068   068   000    -    32 (Min/Max 8/75)\n197 Current_Pending_Sector  -O---K   100   100   000    -    0\n199 UDMA_CRC_Error_Count    -O-RC-   200   199   000    -    0\n240 Unknown_SSD_Attribute   -O---K   100   100   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nGeneral Purpose Log Directory Version 1\nSMART           Log Directory Version 1 [multi-sector log support]\nAddress    Access  R/W   Size  Description\n0x00       GPL,SL  R/O      1  Log Directory\n0x01           SL  R/O      1  Summary SMART error log\n0x02           SL  R/O      1  Comprehensive SMART error log\n0x03       GPL     R/O      2  Ext. Comprehensive SMART error log\n0x04       GPL,SL  R/O      8  Device Statistics log\n0x06           SL  R/O      1  SMART self-test log\n0x07       GPL     R/O      2  Extended self-test log\n0x08           SL  R/O      1  Power Conditions log\n0x09           SL  R/W      1  Selective self-test log\n0x10       GPL     R/O      1  NCQ Command Error log\n0x11       GPL     R/O      1  SATA Phy Event Counters log\n0x18       GPL     -        1  Reserved\n0x1c       GPL     -    32768  Reserved\n0x20       GPL     R/O      7  Streaming performance log [OBS-8]\n0x28       GPL     -    32768  Reserved\n0x2c       GPL     -        1  Reserved\n0x34       GPL     -    32768  Reserved\n0x3c           SL  -      128  Reserved\n0x40       GPL     -        1  Reserved\n0x4c       GPL     -    32768  Reserved\n0x54       GPL     -        1  Reserved\n0x58       GPL     -    32768  Reserved\n0x68       GPL     -        1  Reserved\n0x7c       GPL     -        1  Reserved\n0x80-0x9f  GPL,SL  R/W     16  Host vendor specific log\n0xa0           SL  VS       1  Device vendor specific log\n0xa4       GPL     VS       1  Device vendor specific log\n0xaa       GPL,SL  VS      26  Device vendor specific log\n0xab       GPL,SL  VS       1  Device vendor specific log\n0xb0       GPL,SL  VS     129  Device vendor specific log\n0xb8       GPL     VS       1  Device vendor specific log\n0xcc       GPL     VS       1  Device vendor specific log\n0xd9       GPL     VS     127  Device vendor specific log\n0xe0       GPL     R/W      1  SCT Command/Status\n0xec       GPL,SL  -      129  Reserved\n0xf4       GPL     -        1  Reserved\n\nSMART Extended Comprehensive Error Log Version: 1 (2 sectors)\nNo Errors Logged\n\nSMART Extended Self-test Log Version: 1 (2 sectors)\nNo self-tests have been logged.  [To run self-tests, use: smartctl -t]\n\nSMART Selective self-test log data structure revision number 1\n SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS\n    1        0        0  Not_testing\n    2        0        0  Not_testing\n    3        0        0  Not_testing\n    4        0        0  Not_testing\n    5        0        0  Not_testing\nSelective self-test flags (0x0):\n  After scanning selected spans, do NOT read-scan remainder of disk.\nIf Selective self-test is pending on power-up, resume after 0 minute delay.\n\nSCT Commands not supported\n\nDevice Statistics (GP Log 0x04)\nPage  Offset Size        Value Flags Description\n0x01  =====  =               =  ===  == General Statistics (rev 2) ==\n0x01  0x008  4           12802  ---  Lifetime Power-On Resets\n0x01  0x010  4           10399  ---  Power-on Hours\n0x01  0x018  6     80885243621  ---  Logical Sectors Written\n0x01  0x020  6       968072443  ---  Number of Write Commands\n0x01  0x028  6    100731911036  ---  Logical Sectors Read\n0x01  0x030  6      1755342522  ---  Number of Read Commands\n0x04  =====  =               =  ===  == General Errors Statistics (rev 1) ==\n0x04  0x008  4               0  ---  Number of Reported Uncorrectable Errors\n0x04  0x010  4               0  ---  Resets Between Cmd Acceptance and Completion\n0x06  =====  =               =  ===  == Transport Statistics (rev 1) ==\n0x06  0x008  4               0  ---  Number of Hardware Resets\n0x06  0x010  4               0  ---  Number of ASR Events\n0x06  0x018  4               0  ---  Number of Interface CRC Errors\n0x07  =====  =               =  ===  == Solid State Device Statistics (rev 1) ==\n0x07  0x008  1               0  N--  Percentage Used Endurance Indicator\n                                |||_ C monitored condition met\n                                ||__ D supports DSN\n                                |___ N normalized value\n\nPending Defects log (GP Log 0x0c) not supported\n\nSATA Phy Event Counters (GP Log 0x11)\nID      Size     Value  Description\n0x0001  4            0  Command failed due to ICRC error\n0x000a  4            3  Device-to-host register FISes sent due to a COMRESET\n\n'
		}
	]
	output = read_smartctl(filedir)

	assert expect == output
