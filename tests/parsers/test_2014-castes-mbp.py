#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu
from tests.parsers.read_file import read_file

filedir = "tests/source_files/2014-castes-mbp/"


def test_lspci():
    expect = [{
        "type": "graphics-card",
        "working": "yes",
        "brand-manufacturer": "Nvidia",
        "brand": "Apple Inc.",
        "internal-name": "GK107M",
        "model": "GeForce GT 750M Mac Edition",
        "capacity-byte": 2147483648,
    }]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        True, read_file(filedir, "lspci.txt"), read_file(filedir, "glxinfo.txt")
    )

    assert output == expect


def test_lscpu():
    expect = [{
        "type": "cpu",
        "working": "yes",
        "isa": "x86-64",
        "model": "Core i7-4980HQ",
        "brand": "Intel",
        "core-n": 4,
        "thread-n": 8,
        "frequency-hertz": 2800000000,
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
        "brand": "Apple Inc.",
        "model": "Mac-2BD1B31983FE1663",
        "sn": "C02433601ECG3MK13",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Apple Inc.",
        "model": "Mac-2BD1B31983FE1663",
        "sn": "C02433601ECG3MK13",
        "usb-ports-n": 3,
        "mini-jack-ports-n": 1,
        "hdmi-ports-n": 1,
        "mini-displayport-ports-n": 2,
        "power-connector": "proprietary",
    }
    output = read_dmidecode._get_connectors(
        read_file(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_chassis():
    expect = [{
        "brand": "Apple Inc.",
        "sn": "CENSORED",
        "type": "case",
        "motherboard-form-factor": "proprietary-laptop",
    }]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
