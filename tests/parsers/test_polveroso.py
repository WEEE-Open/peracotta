#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu
from tests.parsers.read_file import read_file

filedir = "tests/source_files/polveroso/"


def test_lspci():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ASUSTeK Computer Inc.",
            "model": "GeForce 9400 GT",
            "internal-name": "G96",  # Missing glxinfo...
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
            "model": "Core 2 Duo E7300",
            "brand": "Intel",
            "core-n": 2,
            "thread-n": 2,
            "frequency-hertz": 2660000000,
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
        "brand": "ASUSTeK Computer INC.",
        "model": "P5QL-E",
        "sn": "MS666999ABCDEF123",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASUSTeK Computer INC.",
        "model": "P5QL-E",
        "sn": "MS666999ABCDEF123",
        "ps2-ports-n": 2,
        "usb-ports-n": 6,
        "serial-ports-n": 1,
        "mini-jack-ports-n": 1,
        "ethernet-ports-n": 1,
        "ide-ports-n": 1,
        "sata-ports-n": 6,
        "esata-ports-n": 1,
        "firewire-ports-n": 2,
        "notes": "Unknown connector: None / Other (AUDIO / AUDIO)",
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    expect = [
        {
            "type": "case",
            "brand": "Chassis Manufacture",
            "sn": "Chassis Serial Number",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
