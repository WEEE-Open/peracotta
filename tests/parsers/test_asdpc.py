#!/usr/bin/env python3

from parsers import (read_decode_dimms, read_dmidecode, read_lscpu,
                     read_lspci_and_glxinfo)
from tests.parsers.read_file import read_file

filedir = "tests/source_files/asdpc/"


def test_lspci():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand-manufacturer": "AMD/ATI",
            "brand": "PC Partner Limited / Sapphire Technology Tahiti PRO",
            "model": "Radeon HD 7950/8950 OEM / R9 280",
            "capacity-byte": 3221225472,
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
            "model": "FX-8370E",
            "brand": "AMD",
            "core-n": 4,
            "thread-n": 8,
            "frequency-hertz": 3300000000,
        }
    ]
    output = read_lscpu.parse_lscpu(read_file(filedir, "lscpu.txt"))

    assert output == expect


def test_ram():
    expect = [
        {
            "ram-ecc": "no",
            "ram-type": "ddr3",
            "brand": "G Skill Intl",
            "capacity-byte": 8589934592,
            "frequency-hertz": 1333000000,
            "model": "F3-1600C7-8GTX",
            "type": "ram",
            "working": "yes",
            "ram-timings": "9-9-9-24",
        },
        {
            "ram-ecc": "no",
            "ram-type": "ddr3",
            "brand": "G Skill Intl",
            "capacity-byte": 8589934592,
            "frequency-hertz": 1333000000,
            "model": "F3-1600C7-8GTX",
            "type": "ram",
            "working": "yes",
            "ram-timings": "9-9-9-24",
        },
    ]
    output = read_decode_dimms.parse_decode_dimms(read_file(filedir, "dimms.txt"))

    assert len(output) == 2, "2 RAM modules are found"
    assert output == expect


def test_baseboard():
    expect = {
        "brand": "Gigabyte Technology Co., Ltd.",
        "model": "970A-DS3P FX",
        "sn": "To be filled by O.E.M",
        "type": "motherboard",
        "working": "yes",
    }
    output = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(read_file(filedir, "baseboard.txt"))

    # This is entirely wrong and is not reflected by any means from reality and the real motherboard, but the manufacturer
    # dropped all this garbage into the DMI information, so here we go...
    expect = {
        "brand": "Gigabyte Technology Co., Ltd.",
        "model": "970A-DS3P FX",
        "type": "motherboard",
        "working": "yes",
        "usb-ports-n": 3,
        "ps2-ports-n": 2,
        "vga-ports-n": 1,
        "serial-ports-n": 1,
        "sn": "To be filled by O.E.M",
        "notes": "Unknown connector: None / Mini Centronics Type-14 (J2A1 / TV Out)\n"
        "Unknown connector: Other / None (J9A1 - TPM HDR / Not Specified)\n"
        "Unknown connector: Other / None (J9C1 - PCIE DOCKING CONN / Not Specified)\n"
        "Unknown connector: Other / None (J6C2 - EXT HDMI / Not Specified)\n"
        "Unknown connector: Other / None (J1D1 - ITP / Not Specified)\n"
        "Unknown connector: Other / None (J9E2 - MDC INTPSR / Not Specified)\n"
        "Unknown connector: Other / None (J9E4 - MDC INTPSR / Not Specified)\n"
        "Unknown connector: Other / None (J9E3 - LPC HOT DOCKING / Not Specified)\n"
        "Unknown connector: Other / None (J9E1 - SCAN MATRIX / Not Specified)\n"
        "Unknown connector: Other / None (J9G1 - LPC SIDE BAND / Not Specified)\n"
        "Unknown connector: Other / None (J8F1 - UNIFIED / Not Specified)\n"
        "Unknown connector: Other / None (J6F1 - LVDS / Not Specified)\n"
        "Unknown connector: Other / None (J2G1 - GFX VID / Not Specified)\n"
        "Unknown connector: Other / None (J1G6 - AC JACK / Not Specified)",
    }
    output = read_dmidecode._get_connectors(read_file(filedir, "connector.txt"), baseboard)

    assert output == expect


def test_chassis():
    # This is also wrong, but for pre-assembled computers it should be right
    expect = [
        {
            "brand": "Gigabyte Technology Co., Ltd.",
            "sn": "To Be Filled By O.E.M",
            "type": "case",
        }
    ]
    output = read_dmidecode.parse_case(read_file(filedir, "chassis.txt"))

    assert output == expect
