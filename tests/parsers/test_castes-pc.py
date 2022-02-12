#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu
from tests.parsers.read_file import read_file

filedir = "tests/source_files/castes-pc/"


def test_lspci():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ZOTAC International (MCO) Ltd.",
            "model": "GeForce GTX 1060 6GB",
            "internal-name": "GP106",
            "capacity-byte": 6442450944,
            "brand-manufacturer": "Nvidia",
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
            "model": "Core i5-6500",
            "brand": "Intel",
            "core-n": 4,
            "thread-n": 4,
            "frequency-hertz": 3200000000,
        }
    ]
    output = read_lscpu.parse_lscpu(read_file(filedir, "lscpu.txt"))

    assert output == expect


def test_ram():
    expect = [
        {
            "type": "ram",
            "working": "yes",
            "brand": "Synertek",
            "ram-ecc": "no",
        },
        {
            "type": "ram",
            "working": "yes",
            "brand": "Synertek",
            "ram-ecc": "no",
        },
    ]
    output = read_decode_dimms.parse_decode_dimms(read_file(filedir, "dimms.txt"))

    assert len(output) == 2, "2 RAM modules are found"
    assert output == expect


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASRock",
        "model": "H110M-ITX/ac",
        "sn": "M80-69017400518",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    # This is entirely wrong and is not reflected by any means from reality and the real motherboard, but the manufacturer
    # dropped all this garbage into the DMI information, so here we go...
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASRock",
        "model": "H110M-ITX/ac",
        "sn": "M80-69017400518",
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    # This is also wrong, but for pre-assembled computers it should be right
    expect = [
        {
            "type": "case",
            "brand": "To Be Filled By O.E.M.",
            "sn": "To Be Filled By O.E.M",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
