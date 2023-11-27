#!/usr/bin/env python3

from peracotta.parsers import read_decode_dimms, read_dmidecode, read_lscpu, read_lspci_and_glxinfo

from tests.parsers.read_file import read_file

filedir = "tests/source_files/Thinkpad-R500/"


def test_lspci():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "Lenovo",
            "model": "Mobile 4 Series Chipset",
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
            "model": "Core 2 Duo P8600",
            "brand": "Intel",
            "core-n": 2,
            "thread-n": 2,
            "frequency-hertz": 2400000000,
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
        "model": "2718V8C",
        "sn": "VQ1FF05G1WA",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "LENOVO",
        "model": "2718V8C",
        "sn": "VQ1FF05G1WA",
        "usb-ports-n": 3,
        "vga-ports-n": 1,
        "mini-jack-ports-n": 2,
        "ethernet-ports-n": 1,
        "firewire-ports-n": 1,
        "rj11-ports-n": 1,
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    expect = [
        {
            "type": "case",
            "brand": "LENOVO",
            "sn": "Not Available",
            "motherboard-form-factor": "proprietary-laptop",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
