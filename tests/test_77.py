#!/usr/bin/env python3

import pytest
# import smartctl
from read_dmidecode import get_baseboard, get_chassis
from read_lspci_and_glxinfo import read_lspci_and_glxinfo

filedir = '77/'


def test_77_lspci():
	expect = {
		'type': 'graphics-card',
		'brand-manufacturer': 'SiS',
		'brand': 'ASUSTeK Computer Inc.',
		'model': '771/671',
		'capacity-byte': None,
		'human_readable_capacity': ''}
	output = read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert output == expect


def test_77_baseboard():
	expect = {
		'brand': 'ASUSTeK Computer INC.',
		'model': 'P5SD2-VM',
		'sn': 'MT721CT11114269',
		'type': 'motherboard'
	}
	output = get_baseboard(filedir + 'baseboard.txt')

	assert output == expect


def test_77_chassis():
	expect = {
		'brand': 'ASUSTeK Computer INC.',
		'model': '',
		'sn': 'MT721CT11114269',
		'type': 'case',
	}
	output = get_chassis(filedir + 'baseboard.txt')

	assert output == expect

# TODO: more tests
