#!/usr/bin/env python3

from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu
from tests.parsers.read_file import read_file

filedir = "tests/source_files/castes-HP-dc7600/"


def test_lspci_dedicated():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "PC Partner Limited / Sapphire Technology",
            "internal-name": "G98",
            "model": "GeForce G 100",
            "capacity-byte": 536870912,  # This has 512 MB of VRAM, but glxinfo reports 496?
            "brand-manufacturer": "Nvidia",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        True,
        read_file(filedir, "NVIDIA-G100/lspci.txt"),
        read_file(filedir, "NVIDIA-G100/glxinfo.txt"),
    )

    assert output == expect


def test_lspci_integrated():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "Hewlett-Packard Company",
            "model": "82945G/GZ",
            "brand-manufacturer": "Intel",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        False,
        read_file(filedir, "82945G/lspci.txt"),
        read_file(filedir, "82945G/glxinfo.txt"),
    )

    assert output == expect


def test_lscpu():
    expect = [
        {
            "type": "cpu",
            "working": "yes",
            "isa": "x86-64",
            "model": "Pentium 4 2.80GHz",
            "brand": "Intel",
            "core-n": 1,
            "thread-n": 2,
            "frequency-hertz": 2800000000,
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
        "brand": "Hewlett-Packard",
        "model": "09F8h",
        "sn": "CZC6203MC5",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

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
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    expect = [
        {
            "type": "case",
            "brand": "Hewlett-Packard",
            "sn": "CZC6203MC5",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
