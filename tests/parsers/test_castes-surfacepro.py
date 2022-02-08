#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu
from tests.parsers.read_file import read_file

filedir = "tests/source_files/castes-SurfacePro4/"


def test_lspci():
    expect = [{
        "type": "graphics-card",
        "working": "yes",
        "brand": "Microsoft Corporation",
        "model": "HD Graphics 515",
        "brand-manufacturer": "Intel",
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
        "model": "Core m3-6Y30",
        "brand": "Intel",
        "core-n": 2,
        "thread-n": 4,
        "frequency-hertz": 900000000,
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
        "brand": "Microsoft Corporation",
        "model": "Surface Pro 4",
        "sn": "A01012111654643A",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Microsoft Corporation",
        "model": "Surface Pro 4",
        "sn": "A01012111654643A",
            }
    output = read_dmidecode._get_connectors(
        read_file(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_chassis():
    expect = [{
        "type": "case",
        "brand": "Microsoft Corporation",
        "sn": "CENSORED",
        "motherboard-form-factor": "proprietary-laptop",
    }]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect


def test_smartctl():
    # TODO: parse this thing
    expect = [
        {
            "type": "hdd",  # Weird smarctl results here... there's no way in the file to tell this is a SSD and not an HDD
            "brand": "Samsung",
            "model": "MZFLV128HCGR-000MV",
            "sn": "S244NX0H985438",
            "capacity-decibyte": -1,  # This is also wrong because whatever
            "spin-rate-rpm": -1,
            "smart-data": "ok",
        }
    ]
    output = read_smartctl.parse_smartctl(read_file(filedir, "smartctl.txt"))

    assert output == expect
