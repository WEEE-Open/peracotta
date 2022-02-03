#!/usr/bin/env python3
import os

from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lscpu
from parsers import read_lspci_and_glxinfo
from parsers import read_smartctl

filedir = "tests/source_files/alecase/"


def test_lspci():
    expect = {
        "brand": "ASUSTeK Computer Inc.",
        "brand-manufacturer": "Nvidia",
        "capacity-byte": 1073741824,
        "internal-name": "GF106",
        "model": "GeForce GTS 450",
        "type": "graphics-card",
        "working": "yes",
    }
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        True, os.path.join(filedir, "lspci.txt"), os.path.join(filedir, "glxinfo.txt")
    )

    assert output == expect


def test_lscpu():
    expect = {
        "brand": "Intel",
        "core-n": 4,
        "frequency-hertz": 3400000000,
        "isa": "x86-64",
        "model": "Core i7-2600",
        "thread-n": 8,
        "type": "cpu",
        "working": "yes",
    }
    output = read_lscpu.parse_lscpu(os.path.join(filedir, "lscpu.txt"))

    assert output == expect


def test_ram():
    expect = [
        {
            "brand": "Micron Technology",
            "capacity-byte": 8589934592,
            "frequency-hertz": 1600000000,
            "model": "CT102464BA160B.C16",
            "ram-ecc": "no",
            "ram-timings": "11-11-11-28",
            "ram-type": "ddr3",
            "sn": "1949761536",
            "type": "ram",
            "working": "yes",
        },
        {
            "brand": "Micron Technology",
            "capacity-byte": 8589934592,
            "frequency-hertz": 1600000000,
            "model": "CT102464BA160B.C16",
            "ram-ecc": "no",
            "ram-timings": "11-11-11-28",
            "ram-type": "ddr3",
            "sn": "2172780544",
            "type": "ram",
            "working": "yes",
        },
    ]
    output = read_decode_dimms.parse_decode_dimms(os.path.join(filedir, "dimms.txt"))

    assert len(output) == 2, "2 RAM modules are found"
    assert output == expect


def test_baseboard():
    expect = {
        "brand": "ASUSTeK Computer INC.",
        "model": "P8H67-M LE",
        "sn": "A5D10110N3",
        "type": "motherboard",
        "working": "yes",
    }
    output = read_dmidecode._get_baseboard(os.path.join(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(os.path.join(filedir, "baseboard.txt"))

    # This is entirely wrong and is not reflected by any means from reality and the real motherboard, but the manufacturer
    # dropped all this garbage into the DMI information, so here we go...
    expect = {
        "brand": "ASUSTeK Computer INC.",
        "ethernet-ports-n": 1,
        "mini-jack-ports-n": 1,
        "model": "P8H67-M LE",
        "notes": "Unknown connector: None / Other (AUDIO / AUDIO)\n"
        "Unknown connector: None / Other (DVI / DVI port)\n"
        "Unknown connector: None / Other (SPDIFO_HDMI / HDMI port)\n"
        "Unknown connector: Other / None (VGA / Not Specified)",
        "ps2-ports-n": 1,
        "sata-ports-n": 6,
        "sn": "A5D10110N3",
        "type": "motherboard",
        "usb-ports-n": 8,
        "working": "yes",
    }
    output = read_dmidecode._get_connectors(
        os.path.join(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_chassis():
    # This is also wrong, but for pre-assembled computers it should be right
    expect = {
        "brand": "Chassis Manufacture",
        "model": "",
        "motherboard-form-factor": "",
        "sn": "Chassis Serial Number",
        "type": "case",
    }
    output = read_dmidecode.parse_case(os.path.join(filedir, "chassis.txt"))

    assert output == expect


def test_smartctl():
    expect = []
    output = read_smartctl.read_smartctl(filedir)

    assert output == expect
