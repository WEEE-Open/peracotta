#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu
from tests.parsers.read_file import read_file

filedir = "tests/source_files/viabork/"


def test_lspci():
    expect = [{
        "type": "graphics-card",
        "working": "yes",
        "brand": "ASUSTeK Computer Inc.",
        "model": "S3 UniChrome Pro",
        "internal-name": "P4M890",
        "brand-manufacturer": "VIA",
    }]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        False, read_file(filedir, "lspci.txt"), read_file(filedir, "glxinfo.txt")
    )

    assert output == expect


def test_lscpu():
    expect = [{
        "type": "cpu",
        "working": "yes",
        "isa": "x86-64",
        "model": "Pentium 4 3.00GHz",
        "brand": "Intel",
        "core-n": 1,
        "thread-n": 2,
        "frequency-hertz": 3000000000,
    }]
    output = read_lscpu.parse_lscpu(read_file(filedir, "lscpu.txt"))

    assert output == expect


def test_ram():
    output = read_decode_dimms.parse_decode_dimms(read_file(filedir, "dimms.txt"))

    assert len(output) == 0


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASUSTeK Computer INC.",
        "model": "P5V-VM-ULTRA",
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
        "model": "P5V-VM-ULTRA",
        "sn": "MB-1234567890",
        "ps2-ports-n": 2,
        "usb-ports-n": 8,
        "parallel-ports-n": 1,
        "serial-ports-n": 1,
        "mini-jack-ports-n": 3,
        "ethernet-ports-n": 1,
        "ide-ports-n": 2,
    }
    output = read_dmidecode._get_connectors(
        read_file(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_chassis():
    expect = [{
        "type": "case",
        "brand": "Chassis Manufacture",
        "sn": "Chassis Serial Number",
    }]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
