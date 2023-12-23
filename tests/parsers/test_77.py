#!/usr/bin/env python3

from peracotta.parsers import read_dmidecode, read_lscpu, read_lspci_and_glxinfo, read_smartctl
from tests.parsers.read_file import read_file

filedir = "tests/source_files/77/"


def test_77_lspci():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand-manufacturer": "SiS",
            "brand": "ASUSTeK Computer Inc.",
            "model": "771/671",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(False, read_file(filedir, "lspci.txt"), read_file(filedir, "glxinfo.txt"))

    assert output == expect


def test_lscpu():
    expect = [
        {
            "type": "cpu",
            "working": "yes",
            "isa": "x86-32",
            "model": "Celeron 2.80GHz",
            "brand": "Intel",
            "core-n": 1,
            "thread-n": 1,
            "frequency-hertz": 2800000000,
        }
    ]
    output = read_lscpu.parse_lscpu(read_file(filedir, "lscpu.txt"))

    assert output == expect


def test_77_baseboard():
    expect = {
        "brand": "ASUSTeK Computer INC.",
        "model": "P5SD2-VM",
        "sn": "MT721CT11114269",
        "type": "motherboard",
        "working": "yes",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_77_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "brand": "ASUSTeK Computer INC.",
        "model": "P5SD2-VM",
        "sn": "MT721CT11114269",
        "type": "motherboard",
        "working": "yes",
        "usb-ports-n": 8,
        "ethernet-ports-n": 1,
        "mini-jack-ports-n": 3,
        "parallel-ports-n": 1,
        "ps2-ports-n": 2,
        "serial-ports-n": 1,
        "ide-ports-n": 1,
        "sata-ports-n": 2,
        "notes": "Unknown connector: Other / None (AAFP / Not Specified)",
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_77_chassis():
    expect = [
        {
            "brand": "Chassis Manufacture",
            "sn": "Chassis Serial Number",
            "type": "case",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect


def test_77_no_disks_disk_that_doesnt_exist():
    expect = []
    output = read_smartctl.parse_smartctl(read_file(filedir, "smartctl.txt"))

    assert output == expect
