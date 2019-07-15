#!/usr/bin/env python3

from read_dmidecode import get_baseboard, get_chassis, get_connectors
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_lscpu import read_lscpu

filedir = 'glxinfo+lspci/'


def test_lspci_dedicated1():
	filesubdir = 'dedicated/NVIDIA6200/'
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "ASUSTeK Computer Inc.",
		'internal-name': 'NV44',
		"model": "GeForce 6200 SE TurboCache",
		"capacity-byte": 67108864,  # 64 MB
		"human_readable_capacity": "53 MB",  # This is reported by glxinfo
		"brand-manufacturer": "Nvidia"
	}

	output = read_lspci_and_glxinfo(True, filedir + filesubdir + 'lspci.txt', filedir + filesubdir + 'glxinfo.txt')

	assert expect == output


def test_lspci_dedicated2():
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "ASUSTeK Computer Inc.",
		'internal-name': 'G96',
		"model": "GeForce 9400 GT",
		"capacity-byte": 1073741824,
		"human_readable_capacity": "1013 MB",
		"brand-manufacturer": "Nvidia"
	}
	output = read_lspci_and_glxinfo(True, filedir + 'dedicated/lspci-9400GT.txt', filedir + 'dedicated/glxinfo-9400GT.txt')

	assert expect == output


def test_lspci_dedicated3():
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "ASUSTeK Computer Inc.",
		'internal-name': 'GM204',
		"model": "GeForce GTX 970",
		"capacity-byte": 4294967296,
		"human_readable_capacity": "4096 MB",
		"brand-manufacturer": "Nvidia"
	}
	output = read_lspci_and_glxinfo(True, filedir + 'dedicated/lspci-gtx-970.txt', filedir + 'dedicated/glxinfo-gtx-970.txt')

	assert expect == output


def test_lspci_integrated_mobo_1():
	filesubdir = 'integrated/on-mobo/'
	file = '8300GT'

	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "ASUSTeK Computer Inc.",
		"model": "GeForce 8300",
		"internal-name": "C77",
		"capacity-byte": None,
		"human_readable_capacity": "",
		"brand-manufacturer": "Nvidia"
	}
	output = read_lspci_and_glxinfo(False, filedir + filesubdir + f'/lspci-{file}.txt', filedir + filesubdir + f'/glxinfo-{file}.txt')

	assert expect == output


def test_lspci_integrated_mobo_2():
	filesubdir = 'integrated/on-mobo/'
	file = '82865G'

	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "Lite-On Technology Corporation",
		"model": "82865G",
		"internal-name": "",
		"capacity-byte": None,
		"human_readable_capacity": "",
		"brand-manufacturer": "Intel"
	}
	output = read_lspci_and_glxinfo(False, filedir + filesubdir + f'/lspci-{file}.txt',
	                                      filedir + filesubdir + f'/glxinfo-{file}.txt')

	assert expect == output


def test_lspci_integrated_mobo_3():
	filesubdir = 'integrated/on-mobo/'
	file = 'ES1000'

	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "Intel Corporation",
		"model": "ES1000",
		"internal-name": "",
		"capacity-byte": None,
		"human_readable_capacity": "",
		"brand-manufacturer": "AMD/ATI"
	}
	output = read_lspci_and_glxinfo(False, filedir + filesubdir + f'/lspci-{file}.txt',
	                                      filedir + filesubdir + f'/glxinfo-{file}.txt')

	assert expect == output


def test_lspci_integrated_cpu_1():
	filesubdir = 'integrated/on-cpu/Acer Swift 3/'

	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "Acer Incorporated",
		"model": "Skylake GT2 [HD Graphics 520]",
		"internal-name": "",
		"capacity-byte": None,
		"human_readable_capacity": "",
		"brand-manufacturer": "Intel"
	}
	output = read_lspci_and_glxinfo(False, filedir + filesubdir + f'/lspci.txt',
	                                      filedir + filesubdir + f'/glxinfo.txt')

	assert expect == output


def test_lspci_integrated_cpu_2():
	filesubdir = 'integrated/on-cpu/HP EliteBook 2540p (i5 M540)/'

	# Yeeeeah, nice and detailed - not.
	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "Hewlett-Packard Company Core Processor",
		"model": "",
		"internal-name": "",
		"capacity-byte": None,
		"human_readable_capacity": "",
		"brand-manufacturer": "Intel"
	}
	output = read_lspci_and_glxinfo(False, filedir + filesubdir + f'/lspci.txt',
	                                      filedir + filesubdir + f'/glxinfo.txt')

	assert expect == output


def test_lspci_integrated_cpu_3():
	filesubdir = 'integrated/on-cpu/Xeon/'

	expect = {
		"type": "graphics-card",
		"working": "yes",
		"brand": "ASRock Incorporation",
		"model": "Xeon E3-1200 v3/4th Gen Core Processor",
		"internal-name": "",
		"capacity-byte": None,
		"human_readable_capacity": "",
		"brand-manufacturer": "Intel"
	}
	output = read_lspci_and_glxinfo(False, filedir + filesubdir + f'/lspci.txt',
	                                      filedir + filesubdir + f'/glxinfo.txt')

	assert expect == output
