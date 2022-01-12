#!/usr/bin/env python3
import os

from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu
from parsers import read_smartctl
import os

filedir = "tests/source_files/77/"


def test_77_lspci():
    expect = {
        "type": "graphics-card",
        "working": "yes",
        "brand-manufacturer": "SiS",
        "brand": "ASUSTeK Computer Inc.",
        "internal-name": "",
        "model": "771/671",
        "capacity-byte": None,
    }
    output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(
        False, os.path.join(filedir, "lspci.txt"), os.path.join(filedir, "glxinfo.txt")
    )

    assert output == expect


def test_lscpu():
    expect = {
        "type": "cpu",
        "working": "yes",
        "isa": "x86-32",
        "model": "Celeron 2.80GHz",
        "brand": "Intel",
        "core-n": 1,
        "thread-n": 1,
        "frequency-hertz": 2800000000,
    }
    output = read_lscpu.read_lscpu(os.path.join(filedir, "lscpu.txt"))

    assert output == expect


def test_77_baseboard():
    expect = {
        "brand": "ASUSTeK Computer INC.",
        "model": "P5SD2-VM",
        "sn": "MT721CT11114269",
        "type": "motherboard",
        "working": "yes",
    }
    output = read_dmidecode.get_baseboard(os.path.join(filedir, "baseboard.txt"))

    assert output == expect


def test_77_connector():
    baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, "baseboard.txt"))

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
    output = read_dmidecode.get_connectors(
        os.path.join(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_77_chassis():
    expect = {
        "brand": "Chassis Manufacture",
        "model": "",
        "sn": "Chassis Serial Number",
        "type": "case",
        "motherboard-form-factor": "",
    }
    output = read_dmidecode.get_chassis(os.path.join(filedir, "chassis.txt"))

    assert output == expect


def test_77_no_disks_disk_that_doesnt_exist():
    expect = []
    output = read_smartctl.read_smartctl(os.path.join(filedir))

    assert output == expect
