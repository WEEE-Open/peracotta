#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'rottame/'


def test_lspci():
	expect = {
		"type": "graphics-card",
		"brand": "ASUSTeK Computer Inc.",
		"model": "GeForce4 MX 440SE AGP 8x",
		"internal-name": "NV18",
		"capacity-byte": -1,  # Missing glxinfo :(
		"human_readable_capacity": "",
		"brand-manufacturer": "Nvidia"
	}
	output = read_lspci_and_glxinfo(True, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"architecture": "x86-64",
		"model": "Pentium D 2.66GHz",
		"brand": "Intel",
		"core-n": 2,
		"thread-n": 2,
		"frequency-hertz": 2660000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu(filedir + 'lscpu.txt')

	assert expect == output


def test_ram():
	expect = [
		{
			"type": "ram",
			"brand": "Kingston",
			"model": "Undefined",
			"sn": "2972574626",
			"frequency-hertz": 533000000,
			"human_readable_frequency": "533 MHz",
			"capacity-byte": 536870912,
			"human_readable_capacity": "512 MB",
			"ram-type": "ddr2",
			"ram-ecc": "no",
			"ram-timings": "5-4-4-12"
		}
	]
	output = read_decode_dimms(filedir + 'dimms.txt')

	assert expect == output


def test_baseboard():
	expect = {
		"type": "motherboard",
		"brand": "ASUSTeK Computer INC.",
		"model": "P5VDC-MX",
		"sn": "MB-1234567890",
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	expect = {
		"type": "motherboard",
		"brand": "ASUSTeK Computer INC.",
		"model": "P5VDC-MX",
		"sn": "MB-1234567890",
		"ps2-ports-n": 2,
		"usb-ports-n": 8,
		"parallel-ports-n": 1,
		"serial-ports-n": 1,
		"vga-ports-n": 1,
		"mini-jack-ports-n": 3,
		"ethernet-ports-n": 1,
		"ide-ports-n": 2,
		"warning": ""
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	# Generic Chassis is generic
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
			"brand": "Maxtor",
			"model": "6V080E0",
			"family": "DiamondMax 10 (SATA/300)",
			"sn": "V66666BG",
			"sata-ports-n": 1,
			"wwn": "0 150500 2ae42de3c",
			"spin-rate-rpm": -1,
			"capacity-decibyte": 82000000000,
			"human_readable_capacity": "81.9 GB",
			"smart-data": "=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x80)\tOffline data collection activity\n\t\t\t\t\twas never started.\n\t\t\t\t\tAuto Offline Data Collection: Enabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t(  901) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x5b) SMART execute Offline immediate.\n\t\t\t\t\tAuto Offline data collection on/off support.\n\t\t\t\t\tSuspend Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tOffline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tNo Conveyance Self-test supported.\n\t\t\t\t\tSelective Self-test supported.\nSMART capabilities:            (0x0003)\tSaves SMART data before entering\n\t\t\t\t\tpower-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tGeneral Purpose Logging supported.\nShort self-test routine \nrecommended polling time: \t (   2) minutes.\nExtended self-test routine\nrecommended polling time: \t (  35) minutes.\nSCT capabilities: \t       (0x0021)\tSCT Status supported.\n\t\t\t\t\tSCT Data Table supported.\n\nSMART Attributes Data Structure revision number: 32\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  3 Spin_Up_Time            POS--K   224   224   063    -    10393\n  4 Start_Stop_Count        -O--CK   253   253   000    -    591\n  5 Reallocated_Sector_Ct   PO--CK   253   253   063    -    0\n  7 Seek_Error_Rate         -O-R--   251   241   000    -    4\n  8 Seek_Time_Performance   POS--K   244   241   187    -    46094\n  9 Power_On_Hours          -O--CK   248   248   000    -    2002\n 10 Spin_Retry_Count        PO-R-K   253   252   157    -    0\n 11 Calibration_Retry_Count PO-R-K   253   252   223    -    0\n 12 Power_Cycle_Count       -O--CK   252   252   000    -    597\n189 High_Fly_Writes         -O-RCK   100   100   000    -    0\n190 Airflow_Temperature_Cel -O---K   067   052   000    -    33 (Min/Max 28/33)\n192 Power-Off_Retract_Count -O--CK   253   253   000    -    0\n193 Load_Cycle_Count        -O--CK   253   253   000    -    0\n194 Temperature_Celsius     -O--CK   038   253   000    -    33\n195 Hardware_ECC_Recovered  -O-R--   253   252   000    -    1026\n196 Reallocated_Event_Count ---R--   253   253   000    -    0\n197 Current_Pending_Sector  ---R--   253   253   000    -    0\n198 Offline_Uncorrectable   ---R--   253   253   000    -    0\n199 UDMA_CRC_Error_Count    ---R--   199   199   000    -    0\n200 Multi_Zone_Error_Rate   -O-R--   253   252   000    -    0\n201 Soft_Read_Error_Rate    -O-R--   253   252   000    -    2\n202 Data_Address_Mark_Errs  -O-R--   253   252   000    -    0\n203 Run_Out_Cancel          PO-R--   253   252   180    -    0\n204 Soft_ECC_Correction     -O-R--   253   252   000    -    0\n205 Thermal_Asperity_Rate   -O-R--   253   252   000    -    0\n207 Spin_High_Current       -O-R-K   253   252   000    -    0\n208 Spin_Buzz               -O-R-K   253   252   000    -    0\n210 Unknown_Attribute       -O--CK   253   252   000    -    0\n211 Unknown_Attribute       -O--CK   253   252   000    -    0\n212 Unknown_Attribute       -O--CK   253   252   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nATA_READ_LOG_EXT (addr=0x00:0x00, page=0, n=1) failed: scsi error badly formed scsi parameters\nRead GP Log Directory failed\n\nSMART Log Directory Version 1 [multi-sector log support]\nAddress    Access  R/W   Size  Description\n0x00           SL  R/O      1  Log Directory\n0x01           SL  R/O      1  Summary SMART error log\n0x02           SL  R/O      1  Comprehensive SMART error log\n0x03           SL  R/O      4  Ext. Comprehensive SMART error log\n0x06           SL  R/O      1  SMART self-test log\n0x09           SL  R/W      1  Selective self-test log\n0x10           SL  R/O      1  SATA NCQ Queued Error log\n0x20           SL  R/O      1  Streaming performance log [OBS-8]\n0x21           SL  R/O      1  Write stream error log\n0x22           SL  R/O      1  Read stream error log\n\nSMART Extended Comprehensive Error Log (GP Log 0x03) not supported\n\nSMART Error Log Version: 1\nNo Errors Logged\n\nSMART Extended Self-test Log (GP Log 0x07) not supported\n\nSMART Self-test log structure revision number 1\nNo self-tests have been logged.  [To run self-tests, use: smartctl -t]\n\nSMART Selective self-test log data structure revision number 1\n SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS\n    1        0        0  Not_testing\n    2        0        0  Not_testing\n    3        0        0  Not_testing\n    4        0        0  Not_testing\n    5        0        0  Not_testing\nSelective self-test flags (0x0):\n  After scanning selected spans, do NOT read-scan remainder of disk.\nIf Selective self-test is pending on power-up, resume after 0 minute delay.\n\nSCT Status Version:                  2\nSCT Version (vendor specific):       1 (0x0001)\nSCT Support Level:                   1\nDevice State:                        Active (0)\nCurrent Temperature:                 33 Celsius\nPower Cycle Max Temperature:         33 Celsius\nLifetime    Max Temperature:         62 Celsius\n\nSCT Temperature History Version:     2\nTemperature Sampling Period:         5 minutes\nTemperature Logging Interval:        5 minutes\nMin/Max recommended Temperature:      0/60 Celsius\nMin/Max Temperature Limit:            0/60 Celsius\nTemperature History Size (Index):    478 (477)\n\nIndex    Estimated Time   Temperature Celsius\n   0    2019-04-01 02:50    39  ********************\n   1    2019-04-01 02:55    38  *******************\n   2    2019-04-01 03:00    39  ********************\n ...    ..( 25 skipped).    ..  ********************\n  28    2019-04-01 05:10    39  ********************\n  29    2019-04-01 05:15    40  *********************\n  30    2019-04-01 05:20    39  ********************\n ...    ..( 13 skipped).    ..  ********************\n  44    2019-04-01 06:30    39  ********************\n  45    2019-04-01 06:35    40  *********************\n  46    2019-04-01 06:40    39  ********************\n  47    2019-04-01 06:45    40  *********************\n  48    2019-04-01 06:50    40  *********************\n  49    2019-04-01 06:55    40  *********************\n  50    2019-04-01 07:00    39  ********************\n ...    ..( 32 skipped).    ..  ********************\n  83    2019-04-01 09:45    39  ********************\n  84    2019-04-01 09:50    40  *********************\n  85    2019-04-01 09:55     ?  -\n  86    2019-04-01 10:00    22  ***\n  87    2019-04-01 10:05     ?  -\n  88    2019-04-01 10:10    27  ********\n  89    2019-04-01 10:15    30  ***********\n  90    2019-04-01 10:20    32  *************\n  91    2019-04-01 10:25    33  **************\n  92    2019-04-01 10:30    34  ***************\n  93    2019-04-01 10:35    35  ****************\n  94    2019-04-01 10:40    36  *****************\n  95    2019-04-01 10:45    37  ******************\n ...    ..( 22 skipped).    ..  ******************\n 118    2019-04-01 12:40    37  ******************\n 119    2019-04-01 12:45    38  *******************\n 120    2019-04-01 12:50    38  *******************\n 121    2019-04-01 12:55    37  ******************\n 122    2019-04-01 13:00    37  ******************\n 123    2019-04-01 13:05    37  ******************\n 124    2019-04-01 13:10    38  *******************\n ...    ..(  2 skipped).    ..  *******************\n 127    2019-04-01 13:25    38  *******************\n 128    2019-04-01 13:30    37  ******************\n 129    2019-04-01 13:35    38  *******************\n ...    ..( 50 skipped).    ..  *******************\n 180    2019-04-01 17:50    38  *******************\n 181    2019-04-01 17:55    39  ********************\n 182    2019-04-01 18:00    38  *******************\n 183    2019-04-01 18:05     ?  -\n 184    2019-04-01 18:10    22  ***\n 185    2019-04-01 18:15     ?  -\n 186    2019-04-01 18:20    27  ********\n 187    2019-04-01 18:25    30  ***********\n 188    2019-04-01 18:30    32  *************\n 189    2019-04-01 18:35    34  ***************\n 190    2019-04-01 18:40    35  ****************\n 191    2019-04-01 18:45    36  *****************\n 192    2019-04-01 18:50    36  *****************\n 193    2019-04-01 18:55    37  ******************\n 194    2019-04-01 19:00    37  ******************\n 195    2019-04-01 19:05    37  ******************\n 196    2019-04-01 19:10    38  *******************\n 197    2019-04-01 19:15    38  *******************\n 198    2019-04-01 19:20    38  *******************\n 199    2019-04-01 19:25    39  ********************\n ...    ..(  6 skipped).    ..  ********************\n 206    2019-04-01 20:00    39  ********************\n 207    2019-04-01 20:05    38  *******************\n 208    2019-04-01 20:10    39  ********************\n 209    2019-04-01 20:15    38  *******************\n 210    2019-04-01 20:20    38  *******************\n 211    2019-04-01 20:25    39  ********************\n ...    ..(  2 skipped).    ..  ********************\n 214    2019-04-01 20:40    39  ********************\n 215    2019-04-01 20:45    38  *******************\n ...    ..(  7 skipped).    ..  *******************\n 223    2019-04-01 21:25    38  *******************\n 224    2019-04-01 21:30    39  ********************\n 225    2019-04-01 21:35    39  ********************\n 226    2019-04-01 21:40    39  ********************\n 227    2019-04-01 21:45    38  *******************\n ...    ..( 10 skipped).    ..  *******************\n 238    2019-04-01 22:40    38  *******************\n 239    2019-04-01 22:45    39  ********************\n ...    ..(  3 skipped).    ..  ********************\n 243    2019-04-01 23:05    39  ********************\n 244    2019-04-01 23:10    38  *******************\n ...    ..(  2 skipped).    ..  *******************\n 247    2019-04-01 23:25    38  *******************\n 248    2019-04-01 23:30    39  ********************\n ...    ..(  9 skipped).    ..  ********************\n 258    2019-04-02 00:20    39  ********************\n 259    2019-04-02 00:25    40  *********************\n 260    2019-04-02 00:30    40  *********************\n 261    2019-04-02 00:35    40  *********************\n 262    2019-04-02 00:40     ?  -\n 263    2019-04-02 00:45    39  ********************\n 264    2019-04-02 00:50     ?  -\n 265    2019-04-02 00:55    40  *********************\n ...    ..(  2 skipped).    ..  *********************\n 268    2019-04-02 01:10    40  *********************\n 269    2019-04-02 01:15    39  ********************\n ...    ..(  7 skipped).    ..  ********************\n 277    2019-04-02 01:55    39  ********************\n 278    2019-04-02 02:00     ?  -\n 279    2019-04-02 02:05    22  ***\n 280    2019-04-02 02:10     ?  -\n 281    2019-04-02 02:15    25  ******\n 282    2019-04-02 02:20    29  **********\n 283    2019-04-02 02:25    31  ************\n 284    2019-04-02 02:30    33  **************\n 285    2019-04-02 02:35    35  ****************\n 286    2019-04-02 02:40    37  ******************\n 287    2019-04-02 02:45    38  *******************\n 288    2019-04-02 02:50    39  ********************\n 289    2019-04-02 02:55    39  ********************\n 290    2019-04-02 03:00     ?  -\n 291    2019-04-02 03:05    22  ***\n 292    2019-04-02 03:10     ?  -\n 293    2019-04-02 03:15    29  **********\n 294    2019-04-02 03:20    31  ************\n 295    2019-04-02 03:25    34  ***************\n 296    2019-04-02 03:30    35  ****************\n 297    2019-04-02 03:35    37  ******************\n 298    2019-04-02 03:40    38  *******************\n 299    2019-04-02 03:45    38  *******************\n 300    2019-04-02 03:50    39  ********************\n 301    2019-04-02 03:55    39  ********************\n 302    2019-04-02 04:00    40  *********************\n ...    ..(  2 skipped).    ..  *********************\n 305    2019-04-02 04:15    40  *********************\n 306    2019-04-02 04:20    41  **********************\n ...    ..(  6 skipped).    ..  **********************\n 313    2019-04-02 04:55    41  **********************\n 314    2019-04-02 05:00    42  ***********************\n ...    ..( 22 skipped).    ..  ***********************\n 337    2019-04-02 06:55    42  ***********************\n 338    2019-04-02 07:00     ?  -\n 339    2019-04-02 07:05    23  ****\n 340    2019-04-02 07:10    21  **\n 341    2019-04-02 07:15    21  **\n 342    2019-04-02 07:20     ?  -\n 343    2019-04-02 07:25    26  *******\n 344    2019-04-02 07:30    29  **********\n 345    2019-04-02 07:35    31  ************\n 346    2019-04-02 07:40     ?  -\n 347    2019-04-02 07:45    24  *****\n 348    2019-04-02 07:50     ?  -\n 349    2019-04-02 07:55    30  ***********\n 350    2019-04-02 08:00    33  **************\n 351    2019-04-02 08:05    35  ****************\n 352    2019-04-02 08:10    37  ******************\n 353    2019-04-02 08:15    38  *******************\n 354    2019-04-02 08:20    39  ********************\n 355    2019-04-02 08:25    39  ********************\n 356    2019-04-02 08:30    40  *********************\n 357    2019-04-02 08:35    40  *********************\n 358    2019-04-02 08:40    40  *********************\n 359    2019-04-02 08:45    41  **********************\n 360    2019-04-02 08:50    41  **********************\n 361    2019-04-02 08:55    41  **********************\n 362    2019-04-02 09:00    42  ***********************\n 363    2019-04-02 09:05    41  **********************\n 364    2019-04-02 09:10    42  ***********************\n ...    ..(  3 skipped).    ..  ***********************\n 368    2019-04-02 09:30    42  ***********************\n 369    2019-04-02 09:35     ?  -\n 370    2019-04-02 09:40    19  -\n 371    2019-04-02 09:45    23  ****\n 372    2019-04-02 09:50     ?  -\n 373    2019-04-02 09:55    27  ********\n 374    2019-04-02 10:00    29  **********\n 375    2019-04-02 10:05    30  ***********\n 376    2019-04-02 10:10    32  *************\n 377    2019-04-02 10:15    33  **************\n 378    2019-04-02 10:20    33  **************\n 379    2019-04-02 10:25    34  ***************\n 380    2019-04-02 10:30    34  ***************\n 381    2019-04-02 10:35    34  ***************\n 382    2019-04-02 10:40    35  ****************\n 383    2019-04-02 10:45    36  *****************\n 384    2019-04-02 10:50    36  *****************\n 385    2019-04-02 10:55    37  ******************\n 386    2019-04-02 11:00    38  *******************\n 387    2019-04-02 11:05    38  *******************\n 388    2019-04-02 11:10    39  ********************\n ...    ..(  2 skipped).    ..  ********************\n 391    2019-04-02 11:25    39  ********************\n 392    2019-04-02 11:30    40  *********************\n 393    2019-04-02 11:35    39  ********************\n 394    2019-04-02 11:40    39  ********************\n 395    2019-04-02 11:45    39  ********************\n 396    2019-04-02 11:50     ?  -\n 397    2019-04-02 11:55    20  *\n 398    2019-04-02 12:00     ?  -\n 399    2019-04-02 12:05    24  *****\n 400    2019-04-02 12:10    28  *********\n 401    2019-04-02 12:15     ?  -\n 402    2019-04-02 12:20    29  **********\n 403    2019-04-02 12:25     ?  -\n 404    2019-04-02 12:30    32  *************\n 405    2019-04-02 12:35    34  ***************\n 406    2019-04-02 12:40    35  ****************\n 407    2019-04-02 12:45    36  *****************\n 408    2019-04-02 12:50    36  *****************\n 409    2019-04-02 12:55    37  ******************\n ...    ..(  2 skipped).    ..  ******************\n 412    2019-04-02 13:10    37  ******************\n 413    2019-04-02 13:15    38  *******************\n 414    2019-04-02 13:20    38  *******************\n 415    2019-04-02 13:25    38  *******************\n 416    2019-04-02 13:30    39  ********************\n 417    2019-04-02 13:35    40  *********************\n 418    2019-04-02 13:40    41  **********************\n ...    ..(  2 skipped).    ..  **********************\n 421    2019-04-02 13:55    41  **********************\n 422    2019-04-02 14:00    40  *********************\n 423    2019-04-02 14:05    39  ********************\n 424    2019-04-02 14:10    39  ********************\n 425    2019-04-02 14:15    38  *******************\n 426    2019-04-02 14:20    38  *******************\n 427    2019-04-02 14:25    38  *******************\n 428    2019-04-02 14:30    39  ********************\n 429    2019-04-02 14:35    38  *******************\n 430    2019-04-02 14:40    39  ********************\n 431    2019-04-02 14:45    39  ********************\n 432    2019-04-02 14:50    39  ********************\n 433    2019-04-02 14:55    40  *********************\n 434    2019-04-02 15:00    40  *********************\n 435    2019-04-02 15:05    41  **********************\n 436    2019-04-02 15:10    41  **********************\n 437    2019-04-02 15:15    41  **********************\n 438    2019-04-02 15:20    42  ***********************\n ...    ..(  6 skipped).    ..  ***********************\n 445    2019-04-02 15:55    42  ***********************\n 446    2019-04-02 16:00    41  **********************\n 447    2019-04-02 16:05    42  ***********************\n ...    ..(  3 skipped).    ..  ***********************\n 451    2019-04-02 16:25    42  ***********************\n 452    2019-04-02 16:30    41  **********************\n 453    2019-04-02 16:35     ?  -\n 454    2019-04-02 16:40    25  ******\n 455    2019-04-02 16:45     ?  -\n 456    2019-04-02 16:50    31  ************\n 457    2019-04-02 16:55    34  ***************\n 458    2019-04-02 17:00    35  ****************\n 459    2019-04-02 17:05    36  *****************\n 460    2019-04-02 17:10    37  ******************\n 461    2019-04-02 17:15     ?  -\n 462    2019-04-02 17:20    22  ***\n 463    2019-04-02 17:25    28  *********\n 464    2019-04-02 17:30     ?  -\n 465    2019-04-02 17:35    32  *************\n 466    2019-04-02 17:40    35  ****************\n 467    2019-04-02 17:45     ?  -\n 468    2019-04-02 17:50    33  **************\n 469    2019-04-02 17:55    33  **************\n 470    2019-04-02 18:00     ?  -\n 471    2019-04-02 18:05    35  ****************\n 472    2019-04-02 18:10     ?  -\n 473    2019-04-02 18:15    35  ****************\n 474    2019-04-02 18:20    28  *********\n 475    2019-04-02 18:25     ?  -\n 476    2019-04-02 18:30    31  ************\n 477    2019-04-02 18:35    33  **************\n\nSCT Error Recovery Control command not supported\n\nDevice Statistics (GP/SMART Log 0x04) not supported\n\nSATA Phy Event Counters (GP Log 0x11) not supported\n\n"
		}

	]
	output = read_smartctl(filedir)

	assert expect == output
