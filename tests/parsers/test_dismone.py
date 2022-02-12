#!/usr/bin/env python3

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu
from tests.parsers.read_file import read_file

filedir = "tests/source_files/dismone/"


def test_lspci():
    # no glxinfo :(
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ASUSTeK Computer Inc.",
            "model": "GeForce GTX 970",
            "internal-name": "GM204",
            "brand-manufacturer": "Nvidia",
        }
    ]
    # False to ignore missing glxinfo
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(False, read_file(filedir, "lspci.txt"), "")

    assert output == expect


def test_lscpu():
    expect = [
        {
            "type": "cpu",
            "working": "yes",
            "isa": "x86-64",
            "model": "Core i7 930",
            "brand": "Intel",
            "core-n": 4,
            "thread-n": 8,
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
        "brand": "ASUSTeK Computer INC.",
        "model": "P6T DELUXE V2",
        "sn": "723627130020069",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASUSTeK Computer INC.",
        "model": "P6T DELUXE V2",
        "sn": "723627130020069",
        "ps2-ports-n": 1,
        "usb-ports-n": 7,
        "firewire-ports-n": 3,
        "ide-ports-n": 1,
        "sata-ports-n": 6,
        "mini-jack-ports-n": 7,
        "ethernet-ports-n": 2,
        "sas-sata-ports-n": 2,
        "notes": "Unknown connector: None / Other (AUDIO / AUDIO)",
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_net_without_connectors():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    expect = [
        {
            "type": "motherboard",
            "working": "yes",
            "brand": "ASUSTeK Computer INC.",
            "model": "P6T DELUXE V2",
            "sn": "723627130020069",
            "ethernet-ports-1000m-n": 2,
            "mac": "00:c0:11:fe:fe:11, 00:c0:11:fe:fe:22",
        }
    ]
    output = read_dmidecode._get_net(read_file(filedir, "net.txt"), baseboard)

    assert output == expect


def test_net_with_connectors():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))
    baseboard = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    expect = [
        {
            "type": "motherboard",
            "working": "yes",
            "brand": "ASUSTeK Computer INC.",
            "model": "P6T DELUXE V2",
            "sn": "723627130020069",
            "ps2-ports-n": 1,
            "usb-ports-n": 7,
            "firewire-ports-n": 3,
            "ide-ports-n": 1,
            "sata-ports-n": 6,
            "mini-jack-ports-n": 7,
            "ethernet-ports-1000m-n": 2,
            "mac": "00:c0:11:fe:fe:11, 00:c0:11:fe:fe:22",
            "sas-sata-ports-n": 2,
            "notes": "Unknown connector: None / Other (AUDIO / AUDIO)",
        }
    ]
    output = read_dmidecode._get_net(read_file(filedir, "net.txt"), baseboard)

    assert output == expect


def test_net_with_connectors_different():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))
    baseboard = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    expect = [
        {
            "type": "motherboard",
            "working": "yes",
            "brand": "ASUSTeK Computer INC.",
            "model": "P6T DELUXE V2",
            "sn": "723627130020069",
            "ps2-ports-n": 1,
            "usb-ports-n": 7,
            "firewire-ports-n": 3,
            "ide-ports-n": 1,
            "sata-ports-n": 6,
            "mini-jack-ports-n": 7,
            "ethernet-ports-1000m-n": 1,
            "ethernet-ports-100m-n": 1,
            "mac": "00:c0:11:fe:fe:11, 00:c0:11:fe:fe:22",
            "sas-sata-ports-n": 2,
            "notes": "Unknown connector: None / Other (AUDIO / AUDIO)",
        }
    ]
    output = read_dmidecode._get_net(read_file(filedir, "net_different.txt"), baseboard)

    assert output == expect


def test_net_with_connectors_too_few():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))
    baseboard = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    expect = [
        {
            "type": "motherboard",
            "working": "yes",
            "brand": "ASUSTeK Computer INC.",
            "model": "P6T DELUXE V2",
            "sn": "723627130020069",
            "ps2-ports-n": 1,
            "usb-ports-n": 7,
            "firewire-ports-n": 3,
            "ide-ports-n": 1,
            "sata-ports-n": 6,
            "mini-jack-ports-n": 7,
            "ethernet-ports-1000m-n": 1,
            "mac": "00:c0:11:fe:fe:22",
            "sas-sata-ports-n": 2,
            "notes": "Unknown connector: None / Other (AUDIO / AUDIO)\n" "BIOS reported 1 more ethernet port that was not found by the kernel",
        }
    ]
    output = read_dmidecode._get_net(read_file(filedir, "net_too_few.txt"), baseboard)

    assert output == expect


def test_net_with_connectors_too_many():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))
    baseboard = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    expect = [
        {
            "type": "motherboard",
            "working": "yes",
            "brand": "ASUSTeK Computer INC.",
            "model": "P6T DELUXE V2",
            "sn": "723627130020069",
            "ps2-ports-n": 1,
            "usb-ports-n": 7,
            "firewire-ports-n": 3,
            "ide-ports-n": 1,
            "sata-ports-n": 6,
            "mini-jack-ports-n": 7,
            "ethernet-ports-1000m-n": 3,
            "mac": "00:c0:11:fe:fe:11, 00:c0:11:fe:fe:22, 00:c0:11:fe:fe:42",
            "sas-sata-ports-n": 2,
            "notes": "Unknown connector: None / Other (AUDIO / AUDIO)",
        }
    ]
    output = read_dmidecode._get_net(read_file(filedir, "net_too_many.txt"), baseboard)

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
