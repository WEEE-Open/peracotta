#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'asdpc/'


def test_lspci():
	expect = {
		'type': 'graphics-card',
		'brand-manufacturer': 'AMD/ATI',
		'internal-name': '',
		'brand': 'PC Partner Limited / Sapphire Technology Tahiti PRO',
		'model': 'Radeon HD 7950/8950 OEM / R9 280',
		'capacity-byte': 3221225472,
		'human_readable_capacity': '3072 MB'
	}
	output = read_lspci_and_glxinfo(True, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"isa": "x86-64",
		"model": "FX-8370E",
		"brand": "AMD",
		"core-n": 4,
		"thread-n": 8,
		"frequency-hertz": 3300000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu(filedir + 'lscpu.txt')

	assert expect == output


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
			'ram-timings': '9-9-9-24',
		}
	]
	output = read_decode_dimms(filedir + 'dimms.txt')

	assert len(output) == 2, "2 RAM modules are found"
	assert expect == output


def test_baseboard():
	expect = {
		'brand': 'Gigabyte Technology Co., Ltd.',
		'model': '970A-DS3P FX',
		'sn': 'To be filled by O.E.M.',
		'type': 'motherboard'
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	# This is entirely wrong and is not reflected by any means from reality and the real motherboard, but the manufacturer
	# dropped all this garbage into the DMI information, so here we go...
	expect = {
		'brand': 'Gigabyte Technology Co., Ltd.',
		'model': '970A-DS3P FX',
		'sn': 'To be filled by O.E.M.',
		'type': 'motherboard',
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
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	# This is also wrong, but for pre-assembled computers it should be right
	expect = {
		'brand': 'Gigabyte Technology Co., Ltd.',
		'model': '',
		'sn': 'To Be Filled By O.E.M.',
		'type': 'case',
		'motherboard-form-factor': '',
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


def test_smartctl():
	expect = [
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
			'smart-data': '=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x00)\tOffline data collection activity\n\t\t\t\t\twas never started.\n\t\t\t\t\tAuto Offline Data Collection: Disabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t(11880) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x7b) SMART execute Offline immediate.\n\t\t\t\t\tAuto Offline data collection on/off support.\n\t\t\t\t\tSuspend Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tOffline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tConveyance Self-test supported.\n\t\t\t\t\tSelective Self-test supported.\nSMART capabilities:            (0x0003)\tSaves SMART data before entering\n\t\t\t\t\tpower-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tGeneral Purpose Logging supported.\nShort self-test routine \nrecommended polling time: \t (   2) minutes.\nExtended self-test routine\nrecommended polling time: \t ( 123) minutes.\nConveyance self-test routine\nrecommended polling time: \t (   5) minutes.\nSCT capabilities: \t       (0x3035)\tSCT Status supported.\n\t\t\t\t\tSCT Feature Control supported.\n\t\t\t\t\tSCT Data Table supported.\n\nSMART Attributes Data Structure revision number: 16\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR-K   200   200   051    -    0\n  3 Spin_Up_Time            POS--K   176   174   021    -    2200\n  4 Start_Stop_Count        -O--CK   094   094   000    -    6158\n  5 Reallocated_Sector_Ct   PO--CK   200   200   140    -    0\n  7 Seek_Error_Rate         -OSR-K   200   200   000    -    0\n  9 Power_On_Hours          -O--CK   084   084   000    -    12016\n 10 Spin_Retry_Count        -O--CK   100   100   000    -    0\n 11 Calibration_Retry_Count -O--CK   100   100   000    -    0\n 12 Power_Cycle_Count       -O--CK   097   097   000    -    3965\n192 Power-Off_Retract_Count -O--CK   200   200   000    -    71\n193 Load_Cycle_Count        -O--CK   198   198   000    -    6086\n194 Temperature_Celsius     -O---K   115   106   000    -    28\n196 Reallocated_Event_Count -O--CK   200   200   000    -    0\n197 Current_Pending_Sector  -O--CK   200   200   000    -    0\n198 Offline_Uncorrectable   ----CK   100   253   000    -    0\n199 UDMA_CRC_Error_Count    -O--CK   200   200   000    -    0\n200 Multi_Zone_Error_Rate   ---R--   100   253   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nGeneral Purpose Log Directory Version 1\nSMART           Log Directory Version 1 [multi-sector log support]\nAddress    Access  R/W   Size  Description\n0x00       GPL,SL  R/O      1  Log Directory\n0x01           SL  R/O      1  Summary SMART error log\n0x02           SL  R/O      5  Comprehensive SMART error log\n0x03       GPL     R/O      6  Ext. Comprehensive SMART error log\n0x06           SL  R/O      1  SMART self-test log\n0x07       GPL     R/O      1  Extended self-test log\n0x09           SL  R/W      1  Selective self-test log\n0x10       GPL     R/O      1  NCQ Command Error log\n0x11       GPL     R/O      1  SATA Phy Event Counters log\n0x80-0x9f  GPL,SL  R/W     16  Host vendor specific log\n0xa0-0xa7  GPL,SL  VS      16  Device vendor specific log\n0xa8-0xb7  GPL,SL  VS       1  Device vendor specific log\n0xbd       GPL,SL  VS       1  Device vendor specific log\n0xc0       GPL,SL  VS       1  Device vendor specific log\n0xc1       GPL     VS      93  Device vendor specific log\n0xe0       GPL,SL  R/W      1  SCT Command/Status\n0xe1       GPL,SL  R/W      1  SCT Data Transfer\n\nSMART Extended Comprehensive Error Log Version: 1 (6 sectors)\nNo Errors Logged\n\nSMART Extended Self-test Log Version: 1 (1 sectors)\nNum  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error\n# 1  Short offline       Completed without error       00%         0         -\n\nSMART Selective self-test log data structure revision number 1\n SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS\n    1        0        0  Not_testing\n    2        0        0  Not_testing\n    3        0        0  Not_testing\n    4        0        0  Not_testing\n    5        0        0  Not_testing\nSelective self-test flags (0x0):\n  After scanning selected spans, do NOT read-scan remainder of disk.\nIf Selective self-test is pending on power-up, resume after 0 minute delay.\n\nSCT Status Version:                  3\nSCT Version (vendor specific):       258 (0x0102)\nDevice State:                        Active (0)\nCurrent Temperature:                    28 Celsius\nPower Cycle Min/Max Temperature:     22/28 Celsius\nLifetime    Min/Max Temperature:     15/37 Celsius\nUnder/Over Temperature Limit Count:   0/0\nVendor specific:\n00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n\nSCT Temperature History Version:     2\nTemperature Sampling Period:         1 minute\nTemperature Logging Interval:        1 minute\nMin/Max recommended Temperature:      0/60 Celsius\nMin/Max Temperature Limit:           -41/85 Celsius\nTemperature History Size (Index):    478 (58)\n\nIndex    Estimated Time   Temperature Celsius\n  59    2019-04-02 07:12    28  *********\n ...    ..(120 skipped).    ..  *********\n 180    2019-04-02 09:13    28  *********\n 181    2019-04-02 09:14     ?  -\n 182    2019-04-02 09:15    22  ***\n 183    2019-04-02 09:16    22  ***\n 184    2019-04-02 09:17    23  ****\n 185    2019-04-02 09:18    23  ****\n 186    2019-04-02 09:19    24  *****\n 187    2019-04-02 09:20    24  *****\n 188    2019-04-02 09:21    25  ******\n 189    2019-04-02 09:22    25  ******\n 190    2019-04-02 09:23    25  ******\n 191    2019-04-02 09:24    26  *******\n ...    ..(  3 skipped).    ..  *******\n 195    2019-04-02 09:28    26  *******\n 196    2019-04-02 09:29    27  ********\n ...    ..(  3 skipped).    ..  ********\n 200    2019-04-02 09:33    27  ********\n 201    2019-04-02 09:34    28  *********\n ...    ..(118 skipped).    ..  *********\n 320    2019-04-02 11:33    28  *********\n 321    2019-04-02 11:34     ?  -\n 322    2019-04-02 11:35    22  ***\n 323    2019-04-02 11:36    22  ***\n 324    2019-04-02 11:37    22  ***\n 325    2019-04-02 11:38    23  ****\n 326    2019-04-02 11:39    23  ****\n 327    2019-04-02 11:40    24  *****\n 328    2019-04-02 11:41    24  *****\n 329    2019-04-02 11:42    25  ******\n 330    2019-04-02 11:43    25  ******\n 331    2019-04-02 11:44    25  ******\n 332    2019-04-02 11:45    26  *******\n ...    ..(  4 skipped).    ..  *******\n 337    2019-04-02 11:50    26  *******\n 338    2019-04-02 11:51    27  ********\n ...    ..(  6 skipped).    ..  ********\n 345    2019-04-02 11:58    27  ********\n 346    2019-04-02 11:59    28  *********\n ...    ..(189 skipped).    ..  *********\n  58    2019-04-02 15:09    28  *********\n\nSCT Error Recovery Control command not supported\n\nDevice Statistics (GP/SMART Log 0x04) not supported\n\nPending Defects log (GP Log 0x0c) not supported\n\nSATA Phy Event Counters (GP Log 0x11)\nID      Size     Value  Description\n0x0001  2            0  Command failed due to ICRC error\n0x0002  2            0  R_ERR response for data FIS\n0x0003  2            0  R_ERR response for device-to-host data FIS\n0x0004  2            0  R_ERR response for host-to-device data FIS\n0x0005  2            0  R_ERR response for non-data FIS\n0x0006  2            0  R_ERR response for device-to-host non-data FIS\n0x0007  2            0  R_ERR response for host-to-device non-data FIS\n0x0008  2            0  Device-to-host non-data FIS retries\n0x0009  2            2  Transition from drive PhyRdy to drive PhyNRdy\n0x000a  2            3  Device-to-host register FISes sent due to a COMRESET\n0x000b  2            0  CRC errors within host-to-device FIS\n0x000f  2            0  R_ERR response for host-to-device data FIS, CRC\n0x0012  2            0  R_ERR response for host-to-device non-data FIS, CRC\n0x8000  4        17207  Vendor specific\n\n'
		},
		{
			'type': 'ssd',
			'brand': 'Samsung',
			'family': 'based SSDs',  # whatever.
			'model': '840 EVO 120GB',
			'sn': 'S1F00F00F00F00',
			'wwn': '5 002538 2c302d451',
			'capacity-byte': 120000000000,
			'human_readable_capacity': '120 GB',
			'smart-data': '=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x00)\tOffline data collection activity\n\t\t\t\t\twas never started.\n\t\t\t\t\tAuto Offline Data Collection: Disabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t( 4200) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x53) SMART execute Offline immediate.\n\t\t\t\t\tAuto Offline data collection on/off support.\n\t\t\t\t\tSuspend Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tNo Offline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tNo Conveyance Self-test supported.\n\t\t\t\t\tSelective Self-test supported.\nSMART capabilities:            (0x0003)\tSaves SMART data before entering\n\t\t\t\t\tpower-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tGeneral Purpose Logging supported.\nShort self-test routine \nrecommended polling time: \t (   2) minutes.\nExtended self-test routine\nrecommended polling time: \t (  70) minutes.\nSCT capabilities: \t       (0x003d)\tSCT Status supported.\n\t\t\t\t\tSCT Error Recovery Control supported.\n\t\t\t\t\tSCT Feature Control supported.\n\t\t\t\t\tSCT Data Table supported.\n\nSMART Attributes Data Structure revision number: 1\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  5 Reallocated_Sector_Ct   PO--CK   100   100   010    -    0\n  9 Power_On_Hours          -O--CK   097   097   000    -    12337\n 12 Power_Cycle_Count       -O--CK   095   095   000    -    4108\n177 Wear_Leveling_Count     PO--C-   095   095   000    -    57\n179 Used_Rsvd_Blk_Cnt_Tot   PO--C-   100   100   010    -    0\n181 Program_Fail_Cnt_Total  -O--CK   100   100   010    -    0\n182 Erase_Fail_Count_Total  -O--CK   100   100   010    -    0\n183 Runtime_Bad_Block       PO--C-   100   100   010    -    0\n187 Uncorrectable_Error_Cnt -O--CK   100   100   000    -    0\n190 Airflow_Temperature_Cel -O--CK   072   058   000    -    28\n195 ECC_Error_Rate          -O-RC-   200   200   000    -    0\n199 CRC_Error_Count         -OSRCK   100   100   000    -    0\n235 POR_Recovery_Count      -O--C-   099   099   000    -    133\n241 Total_LBAs_Written      -O--CK   099   099   000    -    17500329386\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nGeneral Purpose Log Directory Version 1\nSMART           Log Directory Version 1 [multi-sector log support]\nAddress    Access  R/W   Size  Description\n0x00       GPL,SL  R/O      1  Log Directory\n0x01           SL  R/O      1  Summary SMART error log\n0x02           SL  R/O      1  Comprehensive SMART error log\n0x03       GPL     R/O      1  Ext. Comprehensive SMART error log\n0x06           SL  R/O      1  SMART self-test log\n0x07       GPL     R/O      1  Extended self-test log\n0x09           SL  R/W      1  Selective self-test log\n0x10       GPL     R/O      1  NCQ Command Error log\n0x11       GPL     R/O      1  SATA Phy Event Counters log\n0x30       GPL,SL  R/O      9  IDENTIFY DEVICE data log\n0x80-0x9f  GPL,SL  R/W     16  Host vendor specific log\n0xa1       GPL,SL  VS      16  Device vendor specific log\n0xce       GPL,SL  VS      16  Device vendor specific log\n0xe0       GPL,SL  R/W      1  SCT Command/Status\n0xe1       GPL,SL  R/W      1  SCT Data Transfer\n\nSMART Extended Comprehensive Error Log Version: 1 (1 sectors)\nNo Errors Logged\n\nSMART Extended Self-test Log Version: 1 (1 sectors)\nNo self-tests have been logged.  [To run self-tests, use: smartctl -t]\n\nSMART Selective self-test log data structure revision number 1\n SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS\n    1        0        0  Not_testing\n    2        0        0  Not_testing\n    3        0        0  Not_testing\n    4        0        0  Not_testing\n    5        0        0  Not_testing\nSelective self-test flags (0x0):\n  After scanning selected spans, do NOT read-scan remainder of disk.\nIf Selective self-test is pending on power-up, resume after 0 minute delay.\n\nSCT Status Version:                  3\nSCT Version (vendor specific):       1 (0x0001)\nDevice State:                        Active (0)\nCurrent Temperature:                    28 Celsius\nPower Cycle Min/Max Temperature:      ?/ ? Celsius\nLifetime    Min/Max Temperature:      ?/ ? Celsius\nUnder/Over Temperature Limit Count:   0/73707\n\nSCT Temperature History Version:     2\nTemperature Sampling Period:         10 minutes\nTemperature Logging Interval:        10 minutes\nMin/Max recommended Temperature:      ?/ ? Celsius\nMin/Max Temperature Limit:            ?/ ? Celsius\nTemperature History Size (Index):    128 (28)\n\nIndex    Estimated Time   Temperature Celsius\n  29    2019-04-01 17:50     ?  -\n ...    ..( 98 skipped).    ..  -\n   0    2019-04-02 10:20     ?  -\n   1    2019-04-02 10:30    28  *********\n   2    2019-04-02 10:40    27  ********\n   3    2019-04-02 10:50    28  *********\n ...    ..( 16 skipped).    ..  *********\n  20    2019-04-02 13:40    28  *********\n  21    2019-04-02 13:50    27  ********\n  22    2019-04-02 14:00    28  *********\n  23    2019-04-02 14:10    28  *********\n  24    2019-04-02 14:20    29  **********\n  25    2019-04-02 14:30    30  ***********\n  26    2019-04-02 14:40    29  **********\n  27    2019-04-02 14:50    29  **********\n  28    2019-04-02 15:00    28  *********\n\nSCT Error Recovery Control:\n           Read: Disabled\n          Write: Disabled\n\nDevice Statistics (GP/SMART Log 0x04) not supported\n\nPending Defects log (GP Log 0x0c) not supported\n\nSATA Phy Event Counters (GP Log 0x11)\nID      Size     Value  Description\n0x0001  2            0  Command failed due to ICRC error\n0x0002  2            0  R_ERR response for data FIS\n0x0003  2            0  R_ERR response for device-to-host data FIS\n0x0004  2            0  R_ERR response for host-to-device data FIS\n0x0005  2            0  R_ERR response for non-data FIS\n0x0006  2            0  R_ERR response for device-to-host non-data FIS\n0x0007  2            0  R_ERR response for host-to-device non-data FIS\n0x0008  2            0  Device-to-host non-data FIS retries\n0x0009  2            5  Transition from drive PhyRdy to drive PhyNRdy\n0x000a  2            5  Device-to-host register FISes sent due to a COMRESET\n0x000b  2            0  CRC errors within host-to-device FIS\n0x000d  2            0  Non-CRC errors within host-to-device FIS\n0x000f  2            0  R_ERR response for host-to-device data FIS, CRC\n0x0010  2            0  R_ERR response for host-to-device data FIS, non-CRC\n0x0012  2            0  R_ERR response for host-to-device non-data FIS, CRC\n0x0013  2            0  R_ERR response for host-to-device non-data FIS, non-CRC\n\n'
		}
	]
	output = read_smartctl(filedir)

	assert expect == output
