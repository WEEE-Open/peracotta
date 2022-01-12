#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = "tests/source_files/castes-HP-dc7600/"


def test_lspci_dedicated():
    expect = {
        "type": "graphics-card",
        "working": "yes",
        "brand": "PC Partner Limited / Sapphire Technology",
        "internal-name": "G98",
        "model": "GeForce G 100",
        "capacity-byte": 536870912,  # This has 512 MB of VRAM, but glxinfo reports 496?
        "brand-manufacturer": "Nvidia",
    }
    output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(
        True,
        os.path.join(filedir, "NVIDIA-G100/lspci.txt"),
        os.path.join(filedir, "NVIDIA-G100/glxinfo.txt"),
    )

    assert output == expect


def test_lspci_integrated():
    expect = {
        "type": "graphics-card",
        "working": "yes",
        "brand": "Hewlett-Packard Company",
        "model": "82945G/GZ",
        "internal-name": "",
        "capacity-byte": None,
        "brand-manufacturer": "Intel",
    }
    output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(
        False,
        os.path.join(filedir, "82945G/lspci.txt"),
        os.path.join(filedir, "82945G/glxinfo.txt"),
    )

    assert output == expect


def test_lscpu():
    expect = {
        "type": "cpu",
        "working": "yes",
        "isa": "x86-64",
        "model": "Pentium 4 2.80GHz",
        "brand": "Intel",
        "core-n": 1,
        "thread-n": 2,
        "frequency-hertz": 2800000000,
    }
    output = read_lscpu.read_lscpu(os.path.join(filedir, "lscpu.txt"))

    assert output == expect


def test_ram():
    output = read_decode_dimms.read_decode_dimms(os.path.join(filedir, "dimms.txt"))

    assert len(output) == 0


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Hewlett-Packard",
        "model": "09F8h",
        "sn": "CZC6203MC5",
    }
    output = read_dmidecode.get_baseboard(os.path.join(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Hewlett-Packard",
        "model": "09F8h",
        "sn": "CZC6203MC5",
        "ps2-ports-n": 2,
        "usb-ports-n": 8,
        "serial-ports-n": 2,
        "ethernet-ports-n": 1,
        "mini-jack-ports-n": 2,  # Probably wrong, but oh well...
        "ide-ports-n": 1,
        "parallel-ports-n": 1,
        "sata-ports-n": 2,
        "vga-ports-n": 1,
        "notes": "",
    }
    output = read_dmidecode.get_connectors(
        os.path.join(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_chassis():
    expect = {
        "type": "case",
        "brand": "Hewlett-Packard",
        "model": "",
        "sn": "CZC6203MC5",
        "motherboard-form-factor": "",
    }
    output = read_dmidecode.get_chassis(os.path.join(filedir, "chassis.txt"))

    assert output == expect
