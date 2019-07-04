#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'castes-pc/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"brand": "ZOTAC International (MCO) Ltd.",
		"model": "GeForce GTX 1060 6GB",
		'internal-name': 'GP106',
		"capacity-byte": 6442450944,
		"human_readable_capacity": "6144 MB",
		"brand-manufacturer": "Nvidia"
	}
	output = read_lspci_and_glxinfo(True, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"architecture": "x86-64",
		"model": "Core i5-6500",
		"brand": "Intel",
		"core-n": 4,
		"thread-n": 4,
		"frequency-hertz": 3200000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu(filedir + 'lscpu.txt')

	assert expect == output


def test_ram():
	expect = [
		{
			"type": "ram",
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
	output = read_decode_dimms(filedir + 'dimms.txt')

	assert len(output) == 2, "2 RAM modules are found"
	assert expect == output


def test_baseboard():
	expect = {
		"type": "motherboard",
		"brand": "ASRock",
		"model": "H110M-ITX/ac",
		"sn": "M80-69017400518",
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	# This is entirely wrong and is not reflected by any means from reality and the real motherboard, but the manufacturer
	# dropped all this garbage into the DMI information, so here we go...
	expect = {
		"type": "motherboard",
		"brand": "ASRock",
		"model": "H110M-ITX/ac",
		"sn": "M80-69017400518",
		"warning": ""
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	# This is also wrong, but for pre-assembled computers it should be right
	expect = {
		"type": "case",
		"brand": "To Be Filled By O.E.M.",
		"model": "",
		"sn": "To Be Filled By O.E.M.",
		"motherboard-form-factor": ""
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


def test_smartctl():
	expect = [
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
			"smart-data": "=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\nSee vendor-specific Attribute list for marginal Attributes.\n\nGeneral SMART Values:\nOffline data collection status:  (0x82)\tOffline data collection activity\n\t\t\t\t\twas completed without error.\n\t\t\t\t\tAuto Offline Data Collection: Enabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t(    0) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x7b) SMART execute Offline immediate.\n\t\t\t\t\tAuto Offline data collection on/off support.\n\t\t\t\t\tSuspend Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tOffline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tConveyance Self-test supported.\n\t\t\t\t\tSelective Self-test supported.\nSMART capabilities:            (0x0003)\tSaves SMART data before entering\n\t\t\t\t\tpower-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tGeneral Purpose Logging supported.\nShort self-test routine \nrecommended polling time: \t (   2) minutes.\nExtended self-test routine\nrecommended polling time: \t ( 145) minutes.\nConveyance self-test routine\nrecommended polling time: \t (   3) minutes.\nSCT capabilities: \t       (0x303f)\tSCT Status supported.\n\t\t\t\t\tSCT Error Recovery Control supported.\n\t\t\t\t\tSCT Feature Control supported.\n\t\t\t\t\tSCT Data Table supported.\n\nSMART Attributes Data Structure revision number: 10\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR--   119   099   006    -    206410160\n  3 Spin_Up_Time            PO----   098   097   085    -    0\n  4 Start_Stop_Count        -O--CK   099   099   020    -    1940\n  5 Reallocated_Sector_Ct   PO--CK   100   100   036    -    0\n  7 Seek_Error_Rate         POSR--   074   060   030    -    27414184\n  9 Power_On_Hours          -O--CK   098   098   000    -    2017\n 10 Spin_Retry_Count        PO--C-   100   100   097    -    0\n 12 Power_Cycle_Count       -O--CK   100   100   020    -    966\n184 End-to-End_Error        -O--CK   100   100   099    -    0\n187 Reported_Uncorrect      -O--CK   100   100   000    -    0\n188 Command_Timeout         -O--CK   100   100   000    -    1\n189 High_Fly_Writes         -O-RCK   100   100   000    -    0\n190 Airflow_Temperature_Cel -O---K   071   043   045    Past 29 (0 2 29 24 0)\n191 G-Sense_Error_Rate      -O--CK   100   100   000    -    11\n192 Power-Off_Retract_Count -O--CK   100   100   000    -    164\n193 Load_Cycle_Count        -O--CK   018   018   000    -    164806\n194 Temperature_Celsius     -O---K   029   057   000    -    29 (0 19 0 0 0)\n195 Hardware_ECC_Recovered  -O-RC-   119   099   000    -    206410160\n197 Current_Pending_Sector  -O--C-   100   100   000    -    0\n198 Offline_Uncorrectable   ----C-   100   100   000    -    0\n199 UDMA_CRC_Error_Count    -OSRCK   200   200   000    -    0\n240 Head_Flying_Hours       ------   100   253   000    -    1103 (11 165 0)\n241 Total_LBAs_Written      ------   100   253   000    -    2988175193\n242 Total_LBAs_Read         ------   100   253   000    -    711974475\n254 Free_Fall_Sensor        -O--CK   100   100   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nGeneral Purpose Log Directory Version 1\nSMART           Log Directory Version 1 [multi-sector log support]\nAddress    Access  R/W   Size  Description\n0x00       GPL,SL  R/O      1  Log Directory\n0x01       GPL,SL  R/O      1  Summary SMART error log\n0x02       GPL,SL  R/O      5  Comprehensive SMART error log\n0x03       GPL     R/O      5  Ext. Comprehensive SMART error log\n0x06       GPL,SL  R/O      1  SMART self-test log\n0x07       GPL     R/O      1  Extended self-test log\n0x09       GPL,SL  R/W      1  Selective self-test log\n0x10       GPL     R/O      1  NCQ Command Error log\n0x11       GPL     R/O      1  SATA Phy Event Counters log\n0x21       GPL     R/O      1  Write stream error log\n0x22       GPL     R/O      1  Read stream error log\n0x80-0x9f  GPL,SL  R/W     16  Host vendor specific log\n0xa1       GPL,SL  VS      20  Device vendor specific log\n0xa2       GPL     VS    2248  Device vendor specific log\n0xa8       GPL,SL  VS      65  Device vendor specific log\n0xa9       GPL,SL  VS       1  Device vendor specific log\n0xab       GPL     VS       1  Device vendor specific log\n0xae       GPL     VS       1  Device vendor specific log\n0xb0       GPL     VS    2864  Device vendor specific log\n0xbd       GPL     VS     252  Device vendor specific log\n0xbe-0xbf  GPL     VS   65535  Device vendor specific log\n0xe0       GPL,SL  R/W      1  SCT Command/Status\n0xe1       GPL,SL  R/W      1  SCT Data Transfer\n\nSMART Extended Comprehensive Error Log Version: 1 (5 sectors)\nNo Errors Logged\n\nSMART Extended Self-test Log Version: 1 (1 sectors)\nNo self-tests have been logged.  [To run self-tests, use: smartctl -t]\n\nSMART Selective self-test log data structure revision number 1\n SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS\n    1        0        0  Not_testing\n    2        0        0  Not_testing\n    3        0        0  Not_testing\n    4        0        0  Not_testing\n    5        0        0  Not_testing\nSelective self-test flags (0x0):\n  After scanning selected spans, do NOT read-scan remainder of disk.\nIf Selective self-test is pending on power-up, resume after 0 minute delay.\n\nSCT Status Version:                  3\nSCT Version (vendor specific):       522 (0x020a)\nDevice State:                        Active (0)\nCurrent Temperature:                    28 Celsius\nPower Cycle Min/Max Temperature:     24/28 Celsius\nLifetime    Min/Max Temperature:     19/57 Celsius\nSpecified Max Operating Temperature:    36 Celsius\nUnder/Over Temperature Limit Count:   0/0\n\nSCT Temperature History Version:     2\nTemperature Sampling Period:         1 minute\nTemperature Logging Interval:        30 minutes\nMin/Max recommended Temperature:     14/55 Celsius\nMin/Max Temperature Limit:           10/60 Celsius\nTemperature History Size (Index):    128 (72)\n\nIndex    Estimated Time   Temperature Celsius\n  73    2019-04-14 17:00    32  *************\n  74    2019-04-14 17:30     ?  -\n  75    2019-04-14 18:00    24  *****\n  76    2019-04-14 18:30    30  ***********\n  77    2019-04-14 19:00    31  ************\n ...    ..(  4 skipped).    ..  ************\n  82    2019-04-14 21:30    31  ************\n  83    2019-04-14 22:00    30  ***********\n  84    2019-04-14 22:30    30  ***********\n  85    2019-04-14 23:00    31  ************\n  86    2019-04-14 23:30    31  ************\n  87    2019-04-15 00:00     ?  -\n  88    2019-04-15 00:30    24  *****\n  89    2019-04-15 01:00    30  ***********\n  90    2019-04-15 01:30    31  ************\n ...    ..(  3 skipped).    ..  ************\n  94    2019-04-15 03:30    31  ************\n  95    2019-04-15 04:00     ?  -\n  96    2019-04-15 04:30    26  *******\n  97    2019-04-15 05:00    42  ***********************\n  98    2019-04-15 05:30    39  ********************\n  99    2019-04-15 06:00    34  ***************\n 100    2019-04-15 06:30    33  **************\n 101    2019-04-15 07:00    33  **************\n 102    2019-04-15 07:30    34  ***************\n 103    2019-04-15 08:00     ?  -\n 104    2019-04-15 08:30    24  *****\n 105    2019-04-15 09:00    31  ************\n 106    2019-04-15 09:30    31  ************\n 107    2019-04-15 10:00    31  ************\n 108    2019-04-15 10:30    32  *************\n 109    2019-04-15 11:00    31  ************\n 110    2019-04-15 11:30    31  ************\n 111    2019-04-15 12:00    32  *************\n 112    2019-04-15 12:30    32  *************\n 113    2019-04-15 13:00    33  **************\n 114    2019-04-15 13:30    32  *************\n 115    2019-04-15 14:00    33  **************\n 116    2019-04-15 14:30    32  *************\n 117    2019-04-15 15:00    32  *************\n 118    2019-04-15 15:30    31  ************\n 119    2019-04-15 16:00    39  ********************\n 120    2019-04-15 16:30    40  *********************\n 121    2019-04-15 17:00    33  **************\n 122    2019-04-15 17:30    32  *************\n 123    2019-04-15 18:00     ?  -\n 124    2019-04-15 18:30    24  *****\n 125    2019-04-15 19:00    34  ***************\n 126    2019-04-15 19:30    35  ****************\n 127    2019-04-15 20:00    42  ***********************\n   0    2019-04-15 20:30    42  ***********************\n   1    2019-04-15 21:00    42  ***********************\n   2    2019-04-15 21:30     ?  -\n   3    2019-04-15 22:00    24  *****\n   4    2019-04-15 22:30     ?  -\n   5    2019-04-15 23:00    24  *****\n   6    2019-04-15 23:30    40  *********************\n   7    2019-04-16 00:00    33  **************\n   8    2019-04-16 00:30    32  *************\n   9    2019-04-16 01:00     ?  -\n  10    2019-04-16 01:30    25  ******\n  11    2019-04-16 02:00     ?  -\n  12    2019-04-16 02:30    25  ******\n  13    2019-04-16 03:00     ?  -\n  14    2019-04-16 03:30    37  ******************\n  15    2019-04-16 04:00    40  *********************\n  16    2019-04-16 04:30    41  **********************\n  17    2019-04-16 05:00    31  ************\n  18    2019-04-16 05:30    29  **********\n  19    2019-04-16 06:00     ?  -\n  20    2019-04-16 06:30    24  *****\n  21    2019-04-16 07:00    40  *********************\n  22    2019-04-16 07:30    42  ***********************\n  23    2019-04-16 08:00    33  **************\n  24    2019-04-16 08:30    32  *************\n ...    ..(  3 skipped).    ..  *************\n  28    2019-04-16 10:30    32  *************\n  29    2019-04-16 11:00    40  *********************\n  30    2019-04-16 11:30    46  ***************************\n  31    2019-04-16 12:00     ?  -\n  32    2019-04-16 12:30    24  *****\n  33    2019-04-16 13:00    34  ***************\n  34    2019-04-16 13:30    32  *************\n  35    2019-04-16 14:00    32  *************\n  36    2019-04-16 14:30    36  *****************\n  37    2019-04-16 15:00     ?  -\n  38    2019-04-16 15:30    24  *****\n  39    2019-04-16 16:00    32  *************\n  40    2019-04-16 16:30    36  *****************\n  41    2019-04-16 17:00    31  ************\n  42    2019-04-16 17:30     ?  -\n  43    2019-04-16 18:00    24  *****\n  44    2019-04-16 18:30    31  ************\n ...    ..(  2 skipped).    ..  ************\n  47    2019-04-16 20:00    31  ************\n  48    2019-04-16 20:30    32  *************\n  49    2019-04-16 21:00     ?  -\n  50    2019-04-16 21:30    32  *************\n  51    2019-04-16 22:00     ?  -\n  52    2019-04-16 22:30    32  *************\n  53    2019-04-16 23:00     ?  -\n  54    2019-04-16 23:30    32  *************\n  55    2019-04-17 00:00     ?  -\n  56    2019-04-17 00:30    32  *************\n  57    2019-04-17 01:00     ?  -\n  58    2019-04-17 01:30    32  *************\n  59    2019-04-17 02:00    32  *************\n  60    2019-04-17 02:30    33  **************\n  61    2019-04-17 03:00     ?  -\n  62    2019-04-17 03:30    24  *****\n  63    2019-04-17 04:00     ?  -\n  64    2019-04-17 04:30    24  *****\n  65    2019-04-17 05:00     ?  -\n  66    2019-04-17 05:30    24  *****\n  67    2019-04-17 06:00     ?  -\n  68    2019-04-17 06:30    24  *****\n  69    2019-04-17 07:00     ?  -\n  70    2019-04-17 07:30    24  *****\n  71    2019-04-17 08:00     ?  -\n  72    2019-04-17 08:30    24  *****\n\nSCT Error Recovery Control:\n           Read: Disabled\n          Write: Disabled\n\nDevice Statistics (GP/SMART Log 0x04) not supported\n\nPending Defects log (GP Log 0x0c) not supported\n\nSATA Phy Event Counters (GP Log 0x11)\nID      Size     Value  Description\n0x000a  2            4  Device-to-host register FISes sent due to a COMRESET\n0x0001  2            0  Command failed due to ICRC error\n0x0003  2            0  R_ERR response for device-to-host data FIS\n0x0004  2            0  R_ERR response for host-to-device data FIS\n0x0006  2            0  R_ERR response for device-to-host non-data FIS\n0x0007  2            0  R_ERR response for host-to-device non-data FIS\n\n"
		},
		{
			"type": "ssd",
			"brand": "",
			"model": "DREVO X1 SSD",
			"family": "",
			"sn": "TX1711901797",
			"capacity-byte": 240000000000,
			"human_readable_capacity": "240 GB",
			"smart-data": "=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x00)\tOffline data collection activity\n\t\t\t\t\twas never started.\n\t\t\t\t\tAuto Offline Data Collection: Disabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t(  120) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x11) SMART execute Offline immediate.\n\t\t\t\t\tNo Auto Offline data collection support.\n\t\t\t\t\tSuspend Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tNo Offline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tNo Conveyance Self-test supported.\n\t\t\t\t\tNo Selective Self-test supported.\nSMART capabilities:            (0x0002)\tDoes not save SMART data before\n\t\t\t\t\tentering power-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tGeneral Purpose Logging supported.\nShort self-test routine \nrecommended polling time: \t (   2) minutes.\nExtended self-test routine\nrecommended polling time: \t (  10) minutes.\n\nSMART Attributes Data Structure revision number: 1\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     -O--CK   100   100   050    -    0\n  5 Reallocated_Sector_Ct   -O--CK   100   100   050    -    52\n  9 Power_On_Hours          -O--CK   100   100   050    -    1668\n 12 Power_Cycle_Count       -O--CK   100   100   050    -    829\n160 Unknown_Attribute       -O--CK   100   100   050    -    19\n161 Unknown_Attribute       PO--CK   100   100   050    -    35\n163 Unknown_Attribute       -O--CK   100   100   050    -    15\n164 Unknown_Attribute       -O--CK   100   100   050    -    42113\n165 Unknown_Attribute       -O--CK   100   100   050    -    114\n166 Unknown_Attribute       -O--CK   100   100   050    -    10\n167 Unknown_Attribute       -O--CK   100   100   050    -    79\n168 Unknown_Attribute       -O--CK   100   100   050    -    3000\n169 Unknown_Attribute       -O--CK   100   100   050    -    98\n175 Program_Fail_Count_Chip -O--CK   100   100   050    -    0\n176 Erase_Fail_Count_Chip   -O--CK   100   100   050    -    0\n177 Wear_Leveling_Count     -O--CK   100   100   050    -    0\n178 Used_Rsvd_Blk_Cnt_Chip  -O--CK   100   100   050    -    52\n181 Program_Fail_Cnt_Total  -O--CK   100   100   050    -    0\n182 Erase_Fail_Count_Total  -O--CK   100   100   050    -    0\n192 Power-Off_Retract_Count -O--CK   100   100   050    -    68\n194 Temperature_Celsius     -O---K   100   100   050    -    38\n195 Hardware_ECC_Recovered  -O--CK   100   100   050    -    92762\n196 Reallocated_Event_Count -O--CK   100   100   050    -    19\n197 Current_Pending_Sector  -O--CK   100   100   050    -    52\n198 Offline_Uncorrectable   -O--CK   100   100   050    -    19\n199 UDMA_CRC_Error_Count    -O--CK   100   100   050    -    0\n232 Available_Reservd_Space -O--CK   100   100   050    -    35\n241 Total_LBAs_Written      ----CK   100   100   050    -    147066\n242 Total_LBAs_Read         ----CK   100   100   050    -    238128\n245 Unknown_Attribute       -O--CK   100   100   050    -    242467\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nGeneral Purpose Log Directory Version 1\nSMART           Log Directory Version 1 [multi-sector log support]\nAddress    Access  R/W   Size  Description\n0x00       GPL,SL  R/O      1  Log Directory\n0x01           SL  R/O      1  Summary SMART error log\n0x02           SL  R/O      1  Comprehensive SMART error log\n0x03       GPL     R/O      1  Ext. Comprehensive SMART error log\n0x04       GPL,SL  R/O      8  Device Statistics log\n0x06           SL  R/O      1  SMART self-test log\n0x07       GPL     R/O      1  Extended self-test log\n0x10       GPL     R/O      1  NCQ Command Error log\n0x11       GPL     R/O      1  SATA Phy Event Counters log\n0x30       GPL,SL  R/O      9  IDENTIFY DEVICE data log\n0x80-0x9f  GPL,SL  R/W     16  Host vendor specific log\n0xde       GPL     VS       8  Device vendor specific log\n\nSMART Extended Comprehensive Error Log Version: 1 (1 sectors)\nDevice Error Count: 34 (device log contains only the most recent 4 errors)\n\tCR     = Command Register\n\tFEATR  = Features Register\n\tCOUNT  = Count (was: Sector Count) Register\n\tLBA_48 = Upper bytes of LBA High/Mid/Low Registers ]  ATA-8\n\tLH     = LBA High (was: Cylinder High) Register    ]   LBA\n\tLM     = LBA Mid (was: Cylinder Low) Register      ] Register\n\tLL     = LBA Low (was: Sector Number) Register     ]\n\tDV     = Device (was: Device/Head) Register\n\tDC     = Device Control Register\n\tER     = Error register\n\tST     = Status register\nPowered_Up_Time is measured from power on, and printed as\nDDd+hh:mm:SS.sss where DD=days, hh=hours, mm=minutes,\nSS=sec, and sss=millisec. It \"wraps\" after 49.710 days.\n\nError 34 [1] log entry is empty\nError 33 [0] log entry is empty\nError 32 [3] log entry is empty\nError 31 [2] occurred at disk power-on lifetime: 0 hours (0 days + 0 hours)\n  When the command that caused the error occurred, the device was active or idle.\n\n  After command completion occurred, registers were:\n  ER -- ST COUNT  LBA_48  LH LM LL DV DC\n  -- -- -- == -- == == == -- -- -- -- --\n  00 -- 00 00 00 00 00 00 00 00 00 00 00\n\n  Commands leading to the command that caused the error were:\n  CR FEATR COUNT  LBA_48  LH LM LL DV DC  Powered_Up_Time  Command/Feature_Name\n  -- == -- == -- == == == -- -- -- -- --  ---------------  --------------------\n  b0 00 d1 01 01 00 00 4f 00 c2 01 00 08     00:00:00.000  SMART READ ATTRIBUTE THRESHOLDS [OBS-4]\n  2f 00 00 01 01 00 00 00 00 00 03 00 08     00:00:00.000  READ LOG EXT\n  2f 00 00 01 01 00 00 00 00 00 00 00 08     00:00:00.000  READ LOG EXT\n  b0 00 d5 01 01 00 00 4f 00 c2 00 00 08     00:00:00.000  SMART READ LOG\n  b0 00 da 00 00 00 00 4f 00 c2 00 00 08     00:00:00.000  SMART RETURN STATUS\n\nSMART Extended Self-test Log Version: 1 (1 sectors)\nNo self-tests have been logged.  [To run self-tests, use: smartctl -t]\n\nSelective Self-tests/Logging not supported\n\nSCT Commands not supported\n\nDevice Statistics (GP Log 0x04)\nPage  Offset Size        Value Flags Description\n0x01  =====  =               =  ===  == General Statistics (rev 1) ==\n0x01  0x008  4             829  ---  Lifetime Power-On Resets\n0x01  0x010  4            1668  ---  Power-on Hours\n0x01  0x018  6      1048199830  ---  Logical Sectors Written\n0x01  0x020  6       135457893  ---  Number of Write Commands\n0x01  0x028  6      2721079828  ---  Logical Sectors Read\n0x01  0x030  6       215747957  ---  Number of Read Commands\n0x07  =====  =               =  ===  == Solid State Device Statistics (rev 1) ==\n0x07  0x008  1               2  ---  Percentage Used Endurance Indicator\n                                |||_ C monitored condition met\n                                ||__ D supports DSN\n                                |___ N normalized value\n\nPending Defects log (GP Log 0x0c) not supported\n\nSATA Phy Event Counters (GP Log 0x11)\nID      Size     Value  Description\n0x0001  4            0  Command failed due to ICRC error\n0x0002  4            0  R_ERR response for data FIS\n0x0005  4            0  R_ERR response for non-data FIS\n0x000a  4            3  Device-to-host register FISes sent due to a COMRESET\n\n"
		}

	]
	output = read_smartctl(filedir)

	assert expect == output
