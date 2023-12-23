#!/usr/bin/env python3

from peracotta.parsers import read_decode_dimms, read_dmidecode, read_lscpu, read_lspci_and_glxinfo
from tests.parsers.read_file import read_file

filedir = "tests/source_files/2018-castes-mbp/"


def test_lspci():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand-manufacturer": "AMD/ATI",
            "brand": "Apple Inc. Radeon Pro 560X",
            "model": "Radeon RX 460/560D / Pro 450/455/460/555/555X/560/560X",
            "capacity-byte": 4294967296,
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(True, read_file(filedir, "lspci.txt"), read_file(filedir, "glxinfo.txt"))

    assert output == expect


def test_lscpu():
    expect = [
        {
            "type": "cpu",
            "working": "yes",
            "isa": "x86-64",
            "model": "Core i7-8750H",
            "brand": "Intel",
            "core-n": 6,
            "thread-n": 12,
            "frequency-hertz": 2200000000,
        }
    ]
    output = read_lscpu.parse_lscpu(read_file(filedir, "lscpu.txt"))

    assert output == expect


def test_ram():
    output = read_decode_dimms.parse_decode_dimms(read_file(filedir, "dimms.txt"))

    assert len(output) == 0


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Apple Inc.",
        "model": "Mac-937A206F2EE63C01",
        "sn": "C0290440002JP5P1T",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Apple Inc.",
        "model": "Mac-937A206F2EE63C01",
        "sn": "C0290440002JP5P1T",
        "usb-ports-n": 2,
        "mini-jack-ports-n": 1,
        "thunderbolt-ports-n": 1,
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    expect = [
        {
            "brand": "Apple Inc.",
            "sn": "CENSORED",
            "type": "case",
            "motherboard-form-factor": "proprietary-laptop",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
