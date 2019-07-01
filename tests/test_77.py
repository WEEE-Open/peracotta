#!/usr/bin/env python3

import pytest
# import smartctl
from read_decode_dimms import read_decode_dimms
# import read_dmidecode_and_lscpu
from read_lspci_and_glxinfo import read_lspci_and_glxinfo


def test_77_lspci():
	filedir = '77/'

	expect = {
		'type': 'graphics-card',
		'brand-manufacturer': 'SiS',
		'brand': 'ASUSTeK Computer Inc.',
		'model': '771/671',
		'capacity-byte': None,
		'human_readable_capacity': ''}
	output = read_lspci_and_glxinfo(False, filedir + 'lspci.txt', filedir + 'glxinfo.txt')

	assert output == expect
# TODO: more tests
