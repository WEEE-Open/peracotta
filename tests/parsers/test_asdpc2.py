#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu
from tests.parsers.read_file import read_file

filedir = "tests/source_files/asdpc2/"


def test_lspci():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand-manufacturer": "Intel",
            "brand": "ASUSTeK Computer Inc.",
            "model": "HD Graphics 515",
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
            "model": "Core m3-6Y30",
            "brand": "Intel",
            "core-n": 2,
            "thread-n": 4,
            "frequency-hertz": 900000000,
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
        "brand": "ASUSTeK COMPUTER INC.",
        "model": "UX305CA",
        "sn": "BSN12345678901234567",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    # Yep, the connector thing is empty...
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASUSTeK COMPUTER INC.",
        "model": "UX305CA",
        "sn": "BSN12345678901234567",
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    expect = [
        {
            "type": "case",
            "brand": "ASUSTeK COMPUTER INC.",
            "sn": "G6M0DF00361708D",
            "motherboard-form-factor": "proprietary-laptop",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
