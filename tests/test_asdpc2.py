#!/usr/bin/env python3

from read_smartctl import read_smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'asdpc2/'


def test_lspci():
	expect = {
		'type': 'graphics-card',
		"working": "yes",
		'brand-manufacturer': 'Intel',
		'brand': 'ASUSTeK Computer Inc.',
		'internal-name': '',
		'model': 'HD Graphics 515',
		'capacity-byte': None,
		'human_readable_capacity': ''
	}
	output = read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert expect == output


def test_lscpu():
	expect = {
		"type": "cpu",
		"working": "yes",
		"isa": "x86-64",
		"model": "Core m3-6Y30",
		"brand": "Intel",
		"core-n": 2,
		"thread-n": 4,
		"frequency-hertz": 900000000,
		"human_readable_frequency": "N/A"
	}
	output = read_lscpu(filedir + 'lscpu.txt')

	assert expect == output


def test_ram():
	output = read_decode_dimms(filedir + 'dimms.txt')

	assert len(output) == 0


def test_baseboard():
	expect = {
		'type': 'motherboard',
		"working": "yes",
		'brand': 'ASUSTeK COMPUTER INC.',
		'model': 'UX305CA',
		'sn': 'BSN12345678901234567'
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert expect == output


def test_connector():
	baseboard = get_baseboard(filedir + 'baseboard.txt')

	# Yep, the connector thing is empty...
	expect = {
		'type': 'motherboard',
		"working": "yes",
		'brand': 'ASUSTeK COMPUTER INC.',
		'model': 'UX305CA',
		'sn': 'BSN12345678901234567',
		'notes': ''
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert expect == output


def test_chassis():
	expect = {
		'type': 'case',
		'brand': 'ASUSTeK COMPUTER INC.',
		'model': '',
		'sn': 'G6M0DF00361708D',
		'motherboard-form-factor': 'proprietary-laptop'
	}
	output = get_chassis(filedir + 'chassis.txt')

	assert expect == output


def test_smartctl():
	expect = [
		{
			'type': 'ssd',
			'brand': '',
			'model': 'LITEON CV1-8B128',  # This is too much part of the model to extract
			'family': '',
			'sn': 'CV1-8B128_006923456A',
			'wwn': '5 002303 234ddcce5',
			'capacity-byte': 128000000000,
			'human_readable_capacity': '128 GB',
			'human_readable_smart_data': '=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x02)\tOffline data collection activity\n\t\t\t\t\twas completed without error.\n\t\t\t\t\tAuto Offline Data Collection: Disabled.\nSelf-test execution status:      (   0)\tThe previous self-test routine completed\n\t\t\t\t\twithout error or no self-test has ever \n\t\t\t\t\tbeen run.\nTotal time to complete Offline \ndata collection: \t\t(    0) seconds.\nOffline data collection\ncapabilities: \t\t\t (0x11) SMART execute Offline immediate.\n\t\t\t\t\tNo Auto Offline data collection support.\n\t\t\t\t\tSuspend Offline collection upon new\n\t\t\t\t\tcommand.\n\t\t\t\t\tNo Offline surface scan supported.\n\t\t\t\t\tSelf-test supported.\n\t\t\t\t\tNo Conveyance Self-test supported.\n\t\t\t\t\tNo Selective Self-test supported.\nSMART capabilities:            (0x0003)\tSaves SMART data before entering\n\t\t\t\t\tpower-saving mode.\n\t\t\t\t\tSupports SMART auto save timer.\nError logging capability:        (0x01)\tError logging supported.\n\t\t\t\t\tGeneral Purpose Logging supported.\nShort self-test routine \nrecommended polling time: \t (   1) minutes.\nExtended self-test routine\nrecommended polling time: \t (  10) minutes.\nSCT capabilities: \t       (0x003d)\tSCT Status supported.\n\t\t\t\t\tSCT Error Recovery Control supported.\n\t\t\t\t\tSCT Feature Control supported.\n\t\t\t\t\tSCT Data Table supported.\n\nSMART Attributes Data Structure revision number: 1\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR-K   100   100   000    -    0\n  5 Reallocated_Sector_Ct   PO----   100   100   000    -    0\n  9 Power_On_Hours          -O----   100   100   000    -    5\n 12 Power_Cycle_Count       PO----   100   100   000    -    1735\n170 Unknown_Attribute       -O--CK   100   100   000    -    0\n171 Unknown_Attribute       PO----   100   100   000    -    0\n172 Unknown_Attribute       PO----   100   100   000    -    0\n173 Unknown_Attribute       PO----   100   100   000    -    22\n174 Unknown_Attribute       PO----   100   100   000    -    31\n175 Program_Fail_Count_Chip PO----   100   100   000    -    0\n176 Erase_Fail_Count_Chip   PO----   100   100   000    -    0\n177 Wear_Leveling_Count     PO----   100   100   000    -    22\n178 Used_Rsvd_Blk_Cnt_Chip  PO----   100   100   000    -    0\n179 Used_Rsvd_Blk_Cnt_Tot   PO----   100   100   000    -    0\n180 Unused_Rsvd_Blk_Cnt_Tot PO--CK   100   100   000    -    143\n181 Program_Fail_Cnt_Total  PO----   100   100   000    -    0\n182 Erase_Fail_Count_Total  PO----   100   100   000    -    0\n183 Runtime_Bad_Block       -O--CK   100   100   000    -    0\n189 Unknown_SSD_Attribute   ------   100   100   000    -    93\n191 Unknown_SSD_Attribute   ------   100   100   000    -    3\n192 Power-Off_Retract_Count PO----   100   100   000    -    31\n194 Temperature_Celsius     -O----   100   100   000    -    45\n195 Hardware_ECC_Recovered  PO----   100   100   000    -    0\n199 UDMA_CRC_Error_Count    PO----   100   100   000    -    0\n232 Available_Reservd_Space PO----   100   100   010    -    100\n233 Media_Wearout_Indicator PO----   100   100   000    -    88140\n241 Total_LBAs_Written      PO----   100   100   000    -    69582\n242 Total_LBAs_Read         PO----   100   100   000    -    31505\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning\n\nGeneral Purpose Log Directory Version 1\nSMART           Log Directory Version 1 [multi-sector log support]\nAddress    Access  R/W   Size  Description\n0x00       GPL,SL  R/O      1  Log Directory\n0x01       GPL,SL  R/O      1  Summary SMART error log\n0x02       GPL,SL  R/O      1  Comprehensive SMART error log\n0x03       GPL,SL  R/O      1  Ext. Comprehensive SMART error log\n0x04       GPL,SL  R/O      8  Device Statistics log\n0x06       GPL,SL  R/O      1  SMART self-test log\n0x07       GPL,SL  R/O      1  Extended self-test log\n0x09       GPL,SL  R/W      1  Selective self-test log\n0x10       GPL,SL  R/O      1  NCQ Command Error log\n0x11       GPL,SL  R/O      1  SATA Phy Event Counters log\n0x30       GPL,SL  R/O      9  IDENTIFY DEVICE data log\n0x80-0x9f  GPL,SL  R/W     16  Host vendor specific log\n0xe0       GPL,SL  R/W      1  SCT Command/Status\n0xe1       GPL,SL  R/W      1  SCT Data Transfer\n\nSMART Extended Comprehensive Error Log Version: 1 (1 sectors)\nNo Errors Logged\n\nSMART Extended Self-test Log Version: 1 (1 sectors)\nNum  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error\n# 1  Extended offline    Completed without error       00%         3         -\n\nSelective Self-tests/Logging not supported\n\nSCT Status Version:                  3\nSCT Version (vendor specific):       0 (0x0000)\nDevice State:                        Active (0)\nCurrent Temperature:                     0 Celsius\nPower Cycle Min/Max Temperature:     --/ 0 Celsius\nLifetime    Min/Max Temperature:     --/ 0 Celsius\n\nSCT Temperature History Version:     2\nTemperature Sampling Period:         0 minutes\nTemperature Logging Interval:        0 minutes\nMin/Max recommended Temperature:      0/100 Celsius\nMin/Max Temperature Limit:            0/100 Celsius\nTemperature History Size (Index):    128 (127)\n\nIndex    Estimated Time   Temperature Celsius\n   0    2019-04-20 14:57     ?  -\n ...    ..(126 skipped).    ..  -\n 127    2019-04-20 17:04     ?  -\n\nSCT Error Recovery Control:\n           Read: Disabled\n          Write: Disabled\n\nDevice Statistics (GP Log 0x04)\nPage  Offset Size        Value Flags Description\n0x01  =====  =               =  ===  == General Statistics (rev 2) ==\n0x01  0x008  4            1735  ---  Lifetime Power-On Resets\n0x01  0x010  4               5  ---  Power-on Hours\n0x01  0x018  6       265163161  ---  Logical Sectors Written\n0x01  0x020  6        40092297  ---  Number of Write Commands\n0x01  0x028  6      2064763423  ---  Logical Sectors Read\n0x01  0x030  6        24539262  ---  Number of Read Commands\n0x02  =====  =               =  ===  == Free-Fall Statistics (empty) ==\n0x03  =====  =               =  ===  == Rotating Media Statistics (empty) ==\n0x04  =====  =               =  ===  == General Errors Statistics (rev 1) ==\n0x04  0x008  4               0  ---  Number of Reported Uncorrectable Errors\n0x04  0x010  4              37  ---  Resets Between Cmd Acceptance and Completion\n0x05  =====  =               =  ===  == Temperature Statistics (rev 1) ==\n0x05  0x008  1              55  ---  Current Temperature\n0x06  =====  =               =  ===  == Transport Statistics (rev 1) ==\n0x06  0x008  4            4244  ---  Number of Hardware Resets\n0x06  0x018  4               3  ---  Number of Interface CRC Errors\n0x07  =====  =               =  ===  == Solid State Device Statistics (rev 1) ==\n0x07  0x008  1               0  ---  Percentage Used Endurance Indicator\n                                |||_ C monitored condition met\n                                ||__ D supports DSN\n                                |___ N normalized value\n\nPending Defects log (GP Log 0x0c) not supported\n\nSATA Phy Event Counters (GP Log 0x11)\nID      Size     Value  Description\n0x0001  2            0  Command failed due to ICRC error\n0x0002  2            0  R_ERR response for data FIS\n0x0003  2            0  R_ERR response for device-to-host data FIS\n0x0004  2            0  R_ERR response for host-to-device data FIS\n0x0005  2            0  R_ERR response for non-data FIS\n0x0006  2            0  R_ERR response for device-to-host non-data FIS\n0x0007  2            0  R_ERR response for host-to-device non-data FIS\n0x0008  2            0  Device-to-host non-data FIS retries\n0x0009  2            0  Transition from drive PhyRdy to drive PhyNRdy\n0x000a  2            3  Device-to-host register FISes sent due to a COMRESET\n0x000b  2            0  CRC errors within host-to-device FIS\n0x000d  2            0  Non-CRC errors within host-to-device FIS\n0x000f  2            0  R_ERR response for host-to-device data FIS, CRC\n0x0010  2            0  R_ERR response for host-to-device data FIS, non-CRC\n0x0012  2            0  R_ERR response for host-to-device non-data FIS, CRC\n0x0013  2            0  R_ERR response for host-to-device non-data FIS, non-CRC\n\n'}]
	output = read_smartctl(filedir)

	assert expect == output
