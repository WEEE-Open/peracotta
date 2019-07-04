#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'dismone/'


def test_lspci():
	# no glxinfo :(
	expect = {
		"type": "graphics-card",
		"brand": "ASUSTeK Computer Inc.",
		"model": "GeForce GTX 970",
		'internal-name': 'GM204',
		"capacity-byte": -1,
		"human_readable_capacity": "",
		"brand-manufacturer": "Nvidia"
	}
	output = read_lspci_and_glxinfo(True, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"architecture": "x86-64",
		"model": "Core i7 930",
		"brand": "Intel",
		"core-n": 4,
		"thread-n": 8,
		"frequency-hertz": 2800000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu(filedir + 'lscpu.txt')

	assert expect == output


def test_ram():
	output = read_decode_dimms(filedir + 'dimms.txt')

	assert len(output) == 0


def test_baseboard():
	expect = {
		"type": "motherboard",
		"brand": "ASUSTeK Computer INC.",
		"model": "P6T DELUXE V2",
		"sn": "723627130020069",
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
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
		'warning': 'Unknown connector: None / Other (AUDIO / AUDIO)\n'
			'Unknown connector: SAS/SATA Plug Receptacle / None (SAS1 / Not Specified)\n'
			'Unknown connector: SAS/SATA Plug Receptacle / None (SAS2 / Not Specified)'
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	expect = {
		"type": "case",
		"brand": "Chassis Manufacture",
		"model": "",
		"sn": "Chassis Serial Number",
		"motherboard-form-factor": ""
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


def test_smartctl():
	expect = [
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
			"smart-data": "=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x84)\tOffline data collection activity\n\t\t\t\t\twas suspended by an interrupting command from host.\n\t\t\t\t\tAuto Offline Data Collection: Enabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t( 9480) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x7b) SMART execute Offline immediate.\n\t\t\t\t\tAuto Offline data collection on/off support.\n\t\t\t\t\tSuspend Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tOffline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tConveyance Self-test supported.\n\t\t\t\t\tSelective Self-test supported.\nSMART capabilities:            (0x0003)\tSaves SMART data before entering\n\t\t\t\t\tpower-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tGeneral Purpose Logging supported.\nShort self-test routine \nrecommended polling time: \t (   2) minutes.\nExtended self-test routine\nrecommended polling time: \t ( 112) minutes.\nConveyance self-test routine\nrecommended polling time: \t (   5) minutes.\nSCT capabilities: \t       (0x303f)\tSCT Status supported.\n\t\t\t\t\tSCT Error Recovery Control supported.\n\t\t\t\t\tSCT Feature Control supported.\n\t\t\t\t\tSCT Data Table supported.\n\nSMART Attributes Data Structure revision number: 16\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR-K   200   200   051    -    0\n  3 Spin_Up_Time            POS--K   239   228   021    -    1033\n  4 Start_Stop_Count        -O--CK   100   100   000    -    228\n  5 Reallocated_Sector_Ct   PO--CK   200   200   140    -    0\n  7 Seek_Error_Rate         -OSR-K   200   200   000    -    0\n  9 Power_On_Hours          -O--CK   044   044   000    -    41574\n 10 Spin_Retry_Count        -O--CK   100   100   000    -    0\n 11 Calibration_Retry_Count -O--CK   100   100   000    -    0\n 12 Power_Cycle_Count       -O--CK   100   100   000    -    224\n192 Power-Off_Retract_Count -O--CK   200   200   000    -    72\n193 Load_Cycle_Count        -O--CK   200   200   000    -    155\n194 Temperature_Celsius     -O---K   116   105   000    -    31\n196 Reallocated_Event_Count -O--CK   200   200   000    -    0\n197 Current_Pending_Sector  -O--CK   200   200   000    -    0\n198 Offline_Uncorrectable   ----CK   200   200   000    -    0\n199 UDMA_CRC_Error_Count    -O--CK   200   200   000    -    0\n200 Multi_Zone_Error_Rate   ---R--   200   200   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nGeneral Purpose Log Directory Version 1\nSMART           Log Directory Version 1 [multi-sector log support]\nAddress    Access  R/W   Size  Description\n0x00       GPL,SL  R/O      1  Log Directory\n0x01           SL  R/O      1  Summary SMART error log\n0x02           SL  R/O      5  Comprehensive SMART error log\n0x03       GPL     R/O      6  Ext. Comprehensive SMART error log\n0x06           SL  R/O      1  SMART self-test log\n0x07       GPL     R/O      1  Extended self-test log\n0x09           SL  R/W      1  Selective self-test log\n0x10       GPL     R/O      1  SATA NCQ Queued Error log\n0x11       GPL     R/O      1  SATA Phy Event Counters log\n0x80-0x9f  GPL,SL  R/W     16  Host vendor specific log\n0xa0-0xa7  GPL,SL  VS      16  Device vendor specific log\n0xa8-0xb5  GPL,SL  VS       1  Device vendor specific log\n0xb6       GPL     VS       1  Device vendor specific log\n0xb7       GPL,SL  VS       1  Device vendor specific log\n0xc0       GPL,SL  VS       1  Device vendor specific log\n0xc1       GPL     VS      24  Device vendor specific log\n0xe0       GPL,SL  R/W      1  SCT Command/Status\n0xe1       GPL,SL  R/W      1  SCT Data Transfer\n\nSMART Extended Comprehensive Error Log Version: 1 (6 sectors)\nNo Errors Logged\n\nSMART Extended Self-test Log Version: 1 (1 sectors)\nNo self-tests have been logged.  [To run self-tests, use: smartctl -t]\n\nSMART Selective self-test log data structure revision number 1\n SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS\n    1        0        0  Not_testing\n    2        0        0  Not_testing\n    3        0        0  Not_testing\n    4        0        0  Not_testing\n    5        0        0  Not_testing\nSelective self-test flags (0x0):\n  After scanning selected spans, do NOT read-scan remainder of disk.\nIf Selective self-test is pending on power-up, resume after 0 minute delay.\n\nSCT Status Version:                  2\nSCT Version (vendor specific):       258 (0x0102)\nSCT Support Level:                   1\nDevice State:                        SMART Off-line Data Collection executing in background (4)\nCurrent Temperature:                    31 Celsius\nPower Cycle Min/Max Temperature:     23/31 Celsius\nLifetime    Min/Max Temperature:     25/42 Celsius\nUnder/Over Temperature Limit Count:   0/0\n\nSCT Temperature History Version:     2\nTemperature Sampling Period:         1 minute\nTemperature Logging Interval:        1 minute\nMin/Max recommended Temperature:      0/60 Celsius\nMin/Max Temperature Limit:           -41/85 Celsius\nTemperature History Size (Index):    478 (462)\n\nIndex    Estimated Time   Temperature Celsius\n 463    2019-04-16 09:43    31  ************\n ...    ..(137 skipped).    ..  ************\n 123    2019-04-16 12:01    31  ************\n 124    2019-04-16 12:02    32  *************\n ...    ..(181 skipped).    ..  *************\n 306    2019-04-16 15:04    32  *************\n 307    2019-04-16 15:05     ?  -\n 308    2019-04-16 15:06    23  ****\n 309    2019-04-16 15:07    25  ******\n 310    2019-04-16 15:08    25  ******\n 311    2019-04-16 15:09    26  *******\n 312    2019-04-16 15:10    26  *******\n 313    2019-04-16 15:11    27  ********\n 314    2019-04-16 15:12    27  ********\n 315    2019-04-16 15:13    28  *********\n 316    2019-04-16 15:14    28  *********\n 317    2019-04-16 15:15    30  ***********\n ...    ..(  4 skipped).    ..  ***********\n 322    2019-04-16 15:20    30  ***********\n 323    2019-04-16 15:21    31  ************\n ...    ..(138 skipped).    ..  ************\n 462    2019-04-16 17:40    31  ************\n\nSCT Error Recovery Control:\n           Read:     70 (7.0 seconds)\n          Write:     70 (7.0 seconds)\n\nDevice Statistics (GP/SMART Log 0x04) not supported\n\nSATA Phy Event Counters (GP Log 0x11)\nID      Size     Value  Description\n0x0001  2            0  Command failed due to ICRC error\n0x0002  2            0  R_ERR response for data FIS\n0x0003  2            0  R_ERR response for device-to-host data FIS\n0x0004  2            0  R_ERR response for host-to-device data FIS\n0x0005  2            0  R_ERR response for non-data FIS\n0x0006  2            0  R_ERR response for device-to-host non-data FIS\n0x0007  2            0  R_ERR response for host-to-device non-data FIS\n0x000a  2           15  Device-to-host register FISes sent due to a COMRESET\n0x8000  4         1333  Vendor specific\n\n"
		},
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
			"smart-data": "=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x84)\tOffline data collection activity\n\t\t\t\t\twas suspended by an interrupting command from host.\n\t\t\t\t\tAuto Offline Data Collection: Enabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t( 9480) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x7b) SMART execute Offline immediate.\n\t\t\t\t\tAuto Offline data collection on/off support.\n\t\t\t\t\tSuspend Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tOffline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tConveyance Self-test supported.\n\t\t\t\t\tSelective Self-test supported.\nSMART capabilities:            (0x0003)\tSaves SMART data before entering\n\t\t\t\t\tpower-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tGeneral Purpose Logging supported.\nShort self-test routine \nrecommended polling time: \t (   2) minutes.\nExtended self-test routine\nrecommended polling time: \t ( 112) minutes.\nConveyance self-test routine\nrecommended polling time: \t (   5) minutes.\nSCT capabilities: \t       (0x303f)\tSCT Status supported.\n\t\t\t\t\tSCT Error Recovery Control supported.\n\t\t\t\t\tSCT Feature Control supported.\n\t\t\t\t\tSCT Data Table supported.\n\nSMART Attributes Data Structure revision number: 16\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR-K   200   200   051    -    0\n  3 Spin_Up_Time            POS--K   239   230   021    -    1016\n  4 Start_Stop_Count        -O--CK   100   100   000    -    227\n  5 Reallocated_Sector_Ct   PO--CK   200   200   140    -    0\n  7 Seek_Error_Rate         -OSR-K   200   200   000    -    0\n  9 Power_On_Hours          -O--CK   035   035   000    -    47525\n 10 Spin_Retry_Count        -O--CK   100   100   000    -    0\n 11 Calibration_Retry_Count -O--CK   100   100   000    -    0\n 12 Power_Cycle_Count       -O--CK   100   100   000    -    224\n192 Power-Off_Retract_Count -O--CK   200   200   000    -    72\n193 Load_Cycle_Count        -O--CK   200   200   000    -    154\n194 Temperature_Celsius     -O---K   116   104   000    -    31\n196 Reallocated_Event_Count -O--CK   200   200   000    -    0\n197 Current_Pending_Sector  -O--CK   200   200   000    -    0\n198 Offline_Uncorrectable   ----CK   200   200   000    -    0\n199 UDMA_CRC_Error_Count    -O--CK   200   200   000    -    0\n200 Multi_Zone_Error_Rate   ---R--   200   200   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nGeneral Purpose Log Directory Version 1\nSMART           Log Directory Version 1 [multi-sector log support]\nAddress    Access  R/W   Size  Description\n0x00       GPL,SL  R/O      1  Log Directory\n0x01           SL  R/O      1  Summary SMART error log\n0x02           SL  R/O      5  Comprehensive SMART error log\n0x03       GPL     R/O      6  Ext. Comprehensive SMART error log\n0x06           SL  R/O      1  SMART self-test log\n0x07       GPL     R/O      1  Extended self-test log\n0x09           SL  R/W      1  Selective self-test log\n0x10       GPL     R/O      1  SATA NCQ Queued Error log\n0x11       GPL     R/O      1  SATA Phy Event Counters log\n0x80-0x9f  GPL,SL  R/W     16  Host vendor specific log\n0xa0-0xa7  GPL,SL  VS      16  Device vendor specific log\n0xa8-0xb5  GPL,SL  VS       1  Device vendor specific log\n0xb6       GPL     VS       1  Device vendor specific log\n0xb7       GPL,SL  VS       1  Device vendor specific log\n0xc0       GPL,SL  VS       1  Device vendor specific log\n0xc1       GPL     VS      24  Device vendor specific log\n0xe0       GPL,SL  R/W      1  SCT Command/Status\n0xe1       GPL,SL  R/W      1  SCT Data Transfer\n\nSMART Extended Comprehensive Error Log Version: 1 (6 sectors)\nNo Errors Logged\n\nSMART Extended Self-test Log Version: 1 (1 sectors)\nNo self-tests have been logged.  [To run self-tests, use: smartctl -t]\n\nSMART Selective self-test log data structure revision number 1\n SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS\n    1        0        0  Not_testing\n    2        0        0  Not_testing\n    3        0        0  Not_testing\n    4        0        0  Not_testing\n    5        0        0  Not_testing\nSelective self-test flags (0x0):\n  After scanning selected spans, do NOT read-scan remainder of disk.\nIf Selective self-test is pending on power-up, resume after 0 minute delay.\n\nSCT Status Version:                  2\nSCT Version (vendor specific):       258 (0x0102)\nSCT Support Level:                   1\nDevice State:                        SMART Off-line Data Collection executing in background (4)\nCurrent Temperature:                    31 Celsius\nPower Cycle Min/Max Temperature:     23/31 Celsius\nLifetime    Min/Max Temperature:     25/43 Celsius\nUnder/Over Temperature Limit Count:   0/0\n\nSCT Temperature History Version:     2\nTemperature Sampling Period:         1 minute\nTemperature Logging Interval:        1 minute\nMin/Max recommended Temperature:      0/60 Celsius\nMin/Max Temperature Limit:           -41/85 Celsius\nTemperature History Size (Index):    478 (5)\n\nIndex    Estimated Time   Temperature Celsius\n   6    2019-04-16 09:43    31  ************\n ...    ..(187 skipped).    ..  ************\n 194    2019-04-16 12:51    31  ************\n 195    2019-04-16 12:52    32  *************\n 196    2019-04-16 12:53    31  ************\n ...    ..( 69 skipped).    ..  ************\n 266    2019-04-16 14:03    31  ************\n 267    2019-04-16 14:04    32  *************\n ...    ..( 59 skipped).    ..  *************\n 327    2019-04-16 15:04    32  *************\n 328    2019-04-16 15:05     ?  -\n 329    2019-04-16 15:06    23  ****\n 330    2019-04-16 15:07    25  ******\n 331    2019-04-16 15:08    25  ******\n 332    2019-04-16 15:09    26  *******\n 333    2019-04-16 15:10    26  *******\n 334    2019-04-16 15:11    27  ********\n 335    2019-04-16 15:12    27  ********\n 336    2019-04-16 15:13    28  *********\n 337    2019-04-16 15:14    28  *********\n 338    2019-04-16 15:15    30  ***********\n 339    2019-04-16 15:16    30  ***********\n 340    2019-04-16 15:17    30  ***********\n 341    2019-04-16 15:18    31  ************\n ...    ..( 74 skipped).    ..  ************\n 416    2019-04-16 16:33    31  ************\n 417    2019-04-16 16:34    30  ***********\n ...    ..(  9 skipped).    ..  ***********\n 427    2019-04-16 16:44    30  ***********\n 428    2019-04-16 16:45    31  ************\n ...    ..( 37 skipped).    ..  ************\n 466    2019-04-16 17:23    31  ************\n 467    2019-04-16 17:24    32  *************\n 468    2019-04-16 17:25    31  ************\n ...    ..( 14 skipped).    ..  ************\n   5    2019-04-16 17:40    31  ************\n\nSCT Error Recovery Control:\n           Read:     70 (7.0 seconds)\n          Write:     70 (7.0 seconds)\n\nDevice Statistics (GP/SMART Log 0x04) not supported\n\nSATA Phy Event Counters (GP Log 0x11)\nID      Size     Value  Description\n0x0001  2            0  Command failed due to ICRC error\n0x0002  2            0  R_ERR response for data FIS\n0x0003  2            0  R_ERR response for device-to-host data FIS\n0x0004  2            0  R_ERR response for host-to-device data FIS\n0x0005  2            0  R_ERR response for non-data FIS\n0x0006  2            0  R_ERR response for device-to-host non-data FIS\n0x0007  2            0  R_ERR response for host-to-device non-data FIS\n0x000a  2           14  Device-to-host register FISes sent due to a COMRESET\n0x8000  4         1333  Vendor specific\n\n"
		}
	]
	output = read_smartctl(filedir)

	assert expect == output
