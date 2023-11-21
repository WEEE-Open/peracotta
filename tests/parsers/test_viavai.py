#!/usr/bin/env python3

from parsers import (read_decode_dimms, read_dmidecode, read_lscpu,
                     read_lspci_and_glxinfo)
from tests.parsers.read_file import read_file

filedir = "tests/source_files/viavai/"


def test_lspci():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ASUSTeK Computer Inc.",
            "model": "Chrome 9 HC",
            "internal-name": "CN896/VN896/P4M900",
            "brand-manufacturer": "VIA",
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
            "model": "Celeron 2.80GHz",
            "brand": "Intel",
            "core-n": 1,
            "thread-n": 1,
            "frequency-hertz": 2800000000,
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
            "model": "KD6502-ELG",
            "sn": "3072778780",
            "frequency-hertz": 667000000,
            "capacity-byte": 1073741824,
            "ram-type": "ddr2",
            "ram-ecc": "yes",
            "ram-timings": "5-5-5-15",
        }
    ]
    output = read_decode_dimms.parse_decode_dimms(read_file(filedir, "dimms.txt"))

    assert output == expect


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASUSTeK Computer INC.",
        "model": "P5VD2-VM",
        "sn": "123456789000",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASUSTeK Computer INC.",
        "model": "P5VD2-VM",
        "sn": "123456789000",
        "serial-ports-n": 1,
        "parallel-ports-n": 1,
        "usb-ports-n": 8,
        "ps2-ports-n": 2,
        "sata-ports-n": 3,
        "esata-ports-n": 1,
        "vga-ports-n": 1,
        "ethernet-ports-n": 1,
        "mini-jack-ports-n": 3,
        "ide-ports-n": 2,
        "notes": "Unknown connector: None / None (SPDIF_OUT / SPDIF_OUT)",
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    expect = [
        {
            "type": "case",
            "brand": "Chassis Manufacture",
            "sn": "EVAL",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
