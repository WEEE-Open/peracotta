#!/usr/bin/env python3

from peracotta.parsers import read_decode_dimms, read_dmidecode, read_lscpu, read_lspci_and_glxinfo

from tests.parsers.read_file import read_file

filedir = "tests/source_files/rottame/"


def test_lspci():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ASUSTeK Computer Inc.",
            "model": "GeForce4 MX 440SE AGP 8x",
            "internal-name": "NV18",  # Missing glxinfo :(
            "brand-manufacturer": "Nvidia",
        }
    ]
    # False to ignore missing glxinfo
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(False, read_file(filedir, "lspci.txt"), read_file(filedir, "glxinfo.txt"))

    assert output == expect


def test_lscpu():
    expect = [
        {
            "type": "cpu",
            "working": "yes",
            "isa": "x86-64",
            "model": "Pentium D 2.66GHz",
            "brand": "Intel",
            "core-n": 2,
            "thread-n": 2,
            "frequency-hertz": 2660000000,
        }
    ]
    output = read_lscpu.parse_lscpu(read_file(filedir, "lscpu.txt"))

    assert output == expect


def test_ram():
    expect = [
        {
            "type": "ram",
            "working": "yes",
            "brand": "Kingston",
            "sn": "2972574626",
            "frequency-hertz": 533000000,
            "capacity-byte": 536870912,
            "ram-type": "ddr2",
            "ram-ecc": "no",
            "ram-timings": "5-4-4-12",
        }
    ]
    output = read_decode_dimms.parse_decode_dimms(read_file(filedir, "dimms.txt"))

    assert output == expect


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASUSTeK Computer INC.",
        "model": "P5VDC-MX",
        "sn": "MB-1234567890",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
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
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    # Generic Chassis is generic
    expect = [
        {
            "type": "case",
            "brand": "Chassis Manufacture",
            "sn": "Chassis Serial Number",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
