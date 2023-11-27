#!/usr/bin/env python3

from peracotta.parsers import read_decode_dimms, read_dmidecode, read_lscpu, read_lspci_and_glxinfo

from tests.parsers.read_file import read_file

filedir = "tests/source_files/jm11/"


def test_lspci():
    # VGA core graphics processor core VGA processor graphics core VGA processor is the core of this laptop
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "Lenovo 3rd Gen Core processor Graphics Controller",
            "model": "VGA controller",
            "brand-manufacturer": "Intel",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(False, read_file(filedir, "lspci.txt"), read_file(filedir, "glxinfo.txt"))

    assert output == expect


def test_lscpu():
    expect = [
        {
            "type": "cpu",
            "working": "yes",
            "isa": "x86-64",
            "model": "Core i5-3210M",
            "brand": "Intel",
            "core-n": 2,
            "thread-n": 4,
            "frequency-hertz": 2500000000,
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
        "brand": "LENOVO",
        "model": "246837G",
        "sn": "2RTC1A0N333",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "LENOVO",
        "model": "246837G",
        "sn": "2RTC1A0N333",
        "usb-ports-n": 4,
        "vga-ports-n": 1,
        "mini-jack-ports-n": 1,
        "ethernet-ports-n": 1,
        "mini-displayport-ports-n": 1,
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    expect = [
        {
            "type": "case",
            "brand": "LENOVO",
            "sn": "A2K3GED",
            "motherboard-form-factor": "proprietary-laptop",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
