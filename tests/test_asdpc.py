#!/usr/bin/env python3

import pytest
# import smartctl
from read_decode_dimms import read_decode_dimms
from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo

filedir = 'asdpc/'


def test_lspci():
	expect = {
		'type': 'graphics-card',
		'brand-manufacturer': 'AMD/ATI',
		'brand': 'PC Partner Limited / Sapphire Technology Tahiti PRO',
		'model': 'Radeon HD 7950/8950 OEM / R9 280',
		'capacity-byte': 3221225472,
		'human_readable_capacity': '3072 MB'
	}
	output = read_lspci_and_glxinfo(True, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert output == expect


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
	assert output == expect


def test_baseboard():
	expect = {
		'brand': 'Gigabyte Technology Co., Ltd.',
		'model': '970A-DS3P FX',
		'sn': 'To be filled by O.E.M.',
		'type': 'motherboard'
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert output == expect


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
		'serial-ports-n': 1,
		'warning': 'Unknown connector: None / Mini Centronics Type-14\n'
		'Unknown connector: None / DB-15 female\n'
		'Unknown connector: Other / None (J9A1 - TPM HDR / Not Specified)\n'
		'Unknown connector: Other / None (J9C1 - PCIE DOCKING CONN / Not Specified)\n'
		'Unknown connector: Other / None (J2B3 - CPU FAN / Not Specified)\n'
		'Unknown connector: Other / None (J6C2 - EXT HDMI / Not Specified)\n'
		'Unknown connector: Other / None (J3C1 - GMCH FAN / Not Specified)\n'
		'Unknown connector: Other / None (J1D1 - ITP / Not Specified)\n'
		'Unknown connector: Other / None (J9E2 - MDC INTPSR / Not Specified)\n'
		'Unknown connector: Other / None (J9E4 - MDC INTPSR / Not Specified)\n'
		'Unknown connector: Other / None (J9E3 - LPC HOT DOCKING / Not Specified)\n'
		'Unknown connector: Other / None (J9E1 - SCAN MATRIX / Not Specified)\n'
		'Unknown connector: Other / None (J9G1 - LPC SIDE BAND / Not Specified)\n'
		'Unknown connector: Other / None (J8F1 - UNIFIED / Not Specified)\n'
		'Unknown connector: Other / None (J6F1 - LVDS / Not Specified)\n'
		'Unknown connector: Other / None (J2F1 - LAI FAN / Not Specified)\n'
		'Unknown connector: Other / None (J2G1 - GFX VID / Not Specified)\n'
		'Unknown connector: Other / None (J1G6 - AC JACK / Not Specified)',
	}
	output = get_connectors(filedir + 'connector.txt', baseboard)

	assert output == expect


def test_chassis():
	# This is also wrong, but for pre-assembled computers it should be right
	expect = {
		'brand': 'Gigabyte Technology Co., Ltd.',
		'model': '',
		'sn': 'To be filled by O.E.M.',
		'type': 'case',
	}
	output = get_chassis(filedir + 'baseboard.txt')

	assert output == expect

# TODO: more tests
