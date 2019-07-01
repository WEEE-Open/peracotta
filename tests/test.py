#!/usr/bin/env python3

import pytest
# import smartctl
from read_decode_dimms import read_decode_dimms
# import read_dmidecode_and_lscpu
from read_lspci_and_glxinfo import read_lspci_and_glxinfo


def test_77():
	filedir = '77/'

	expect = {
		'type': 'graphics-card',
		'brand-manufacturer': 'SiS',
		'brand': 'ASUSTek Computer Inc.',
		'model': '771/671',
		'capacity-byte': None,
		'human_readable_capacity': ''}
	output = read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert output == expect
	# TODO: more tests


def test_asdpc():
	dir = 'asdpc/'

	expect = {
		'type': 'graphics-card',
		'brand-manufacturer': 'AMD/ATI',
		'brand': 'PC Partner Limited / Sapphire Technology Tahiti PRO',
		'model': 'Radeon HD 7950/8950 OEM / R9 280',
		'capacity-byte': 3221225472,
		'human_readable_capacity': '3072 MB'
	}
	output = read_lspci_and_glxinfo(True, dir + 'lspci.txt', dir + 'glxinfo.txt')

	assert output == expect

	expect = [
		{
			'ECC': 'no',
			'RAM_type': 'ddr3',
			'brand': 'G Skill Intl',
			'capacity': 8589934592,
			'frequency': 1333000000,
			'human_readable_capacity': '8192 MB',
			'human_readable_frequency': '1333 MHz',
			'model': 'F3-1600C7-8GTX',
			'serial_number': '',
			'type': 'ram'
		},
		{
			'ECC': 'no',
			'RAM_type': 'ddr3',
			'brand': 'G Skill Intl',
			'capacity': 8589934592,
			'frequency': 1333000000,
			'human_readable_capacity': '8192 MB',
			'human_readable_frequency': '1333 MHz',
			'model': 'F3-1600C7-8GTX',
			'serial_number': '',
			'type': 'ram'
		}
	]
	output = read_decode_dimms(dir + 'dimms.txt')

	assert output == expect
	# TODO: more tests
