#!/usr/bin/env python3

from peracotta.parsers import read_decode_dimms, read_dmidecode, read_lscpu, read_lspci_and_glxinfo
from tests.parsers.read_file import read_file

filedir = "tests/source_files/travasato/"


def test_lspci():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ASUSTeK Computer Inc.",
            "model": "GeForce GT 610",
            "internal-name": "GF119",  # Still no glxinfo :(
            "brand-manufacturer": "Nvidia",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(False, read_file(filedir, "lspci.txt"), "")

    assert output == expect


def test_lscpu():
    expect = [
        {
            "type": "cpu",
            "working": "yes",
            "isa": "x86-64",
            "model": "Core 2 Quad Q6600",
            "brand": "Intel",
            "core-n": 4,
            "thread-n": 4,
            "frequency-hertz": 2400000000,
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
            "model": "K",
            "sn": "3375612238",
            "frequency-hertz": 667000000,
            "capacity-byte": 2147483648,
            "ram-type": "ddr2",
            "ram-ecc": "yes",
            "ram-timings": "5-5-5-15",
        },
        {
            "type": "ram",
            "working": "yes",
            "brand": "Kingston",
            "model": "K",
            "sn": "3392385358",
            "frequency-hertz": 667000000,
            "capacity-byte": 2147483648,
            "ram-type": "ddr2",
            "ram-ecc": "yes",
            "ram-timings": "5-5-5-15",
        },
    ]
    output = read_decode_dimms.parse_decode_dimms(read_file(filedir, "dimms.txt"))

    assert output == expect


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Intel Corporation",
        "model": "D975XBX2",
        "sn": "BAOB4B9001YY",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Intel Corporation",
        "model": "D975XBX2",
        "sn": "BAOB4B9001YY",
        "ide-ports-n": 2,
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    # At least it's not assuming stuff it cannot know...
    expect = [
        {
            "type": "case",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
