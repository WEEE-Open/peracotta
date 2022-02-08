#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu
from tests.parsers.read_file import read_file

filedir = "tests/source_files/cassone/"


def test_lspci():
    expect = [{
        "type": "graphics-card",
        "working": "yes",
        "brand": "SiS",
        "model": "65x/M650/740",
    }]

    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        False, read_file(filedir, "lspci.txt"), read_file(filedir, "glxinfo.txt")
    )

    assert output == expect


def test_lscpu():
    expect = [{
        "type": "cpu",
        "working": "yes",
        "isa": "x86-32",
        "model": "Athlon 4",
        "brand": "AMD",
        "core-n": 1,
        "thread-n": 1,
        "frequency-hertz": "1.24 GHz",
    }]

    output = read_lscpu.parse_lscpu(read_file(filedir, "lscpu.txt"))

    assert output == expect


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Matsonic",
        "model": "MS8318E",
        "sn": "00000000",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Matsonic",
        "model": "MS8318E",
        "sn": "00000000",
        "parallel-ports-n": 1,
    }

    output = read_dmidecode._get_connectors(
        read_file(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_chassis():
    expect = [{
        "type": "case",
        "brand": "Matsonic",
    }]

    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect


def test_smartctl():
    output = read_smartctl.parse_smartctl(read_file(filedir, "smartctl.txt"))

    assert 0 == len(output)
