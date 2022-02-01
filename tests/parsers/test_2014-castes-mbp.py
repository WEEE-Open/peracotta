#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = "tests/source_files/2014-castes-mbp/"


def test_lspci():
    expect = {
        "type": "graphics-card",
        "working": "yes",
        "brand-manufacturer": "Nvidia",
        "brand": "Apple Inc.",
        "internal-name": "GK107M",
        "model": "GeForce GT 750M Mac Edition",
        "capacity-byte": 2147483648,
    }
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        True, os.path.join(filedir, "lspci.txt"), os.path.join(filedir, "glxinfo.txt")
    )

    assert output == expect


def test_lscpu():
    expect = {
        "type": "cpu",
        "working": "yes",
        "isa": "x86-64",
        "model": "Core i7-4980HQ",
        "brand": "Intel",
        "core-n": 4,
        "thread-n": 8,
        "frequency-hertz": 2800000000,
    }
    output = read_lscpu.parse_lscpu(os.path.join(filedir, "lscpu.txt"))

    assert output == expect


def test_ram():
    output = read_decode_dimms.parse_decode_dimms(os.path.join(filedir, "dimms.txt"))

    assert len(output) == 0


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Apple Inc.",
        "model": "Mac-2BD1B31983FE1663",
        "sn": "C02433601ECG3MK13",
    }
    output = read_dmidecode.get_baseboard(os.path.join(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, "baseboard.txt"))

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
        "notes": "",
    }
    output = read_dmidecode.get_connectors(
        os.path.join(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_chassis():
    expect = {
        "brand": "Apple Inc.",
        "sn": "CENSORED",
        "type": "case",
        "motherboard-form-factor": "proprietary-laptop",
        "model": "",
    }
    output = read_dmidecode.parse_case(os.path.join(filedir, "chassis.txt"))

    assert output == expect


def test_smartctl():
    expect = [
        {
            "type": "ssd",
            "brand": "Apple",
            "family": "SD/SM/TS...E/F/G SSDs",
            "model": "SM0512F",
            "sn": "S1K5NYCF740776",
            "capacity-byte": 500000000000,
            "wwn": "5 002538 655584d30",
            "smart-data": "ok",
            "sata-ports-n": 1,
            "notes": "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     -O-RC-   200   200   000    -    0\n  5 Reallocated_Sector_Ct   PO--CK   100   100   000    -    0\n  9 Power_On_Hours          -O--CK   097   097   000    -    10399\n 12 Power_Cycle_Count       -O--CK   087   087   000    -    12802\n169 Unknown_Apple_Attrib    PO--C-   253   253   010    -    3312107658752\n173 Wear_Leveling_Count     -O--CK   186   186   100    -    584144191767\n174 Host_Reads_MiB          -O---K   099   099   000    -    49185503\n175 Host_Writes_MiB         -O---K   099   099   000    -    39494747\n192 Power-Off_Retract_Count -O--C-   099   099   000    -    254\n194 Temperature_Celsius     -O---K   068   068   000    -    32 (Min/Max 8/75)\n197 Current_Pending_Sector  -O---K   100   100   000    -    0\n199 UDMA_CRC_Error_Count    -O-RC-   200   199   000    -    0\n240 Unknown_SSD_Attribute   -O---K   100   100   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning",
        }
    ]
    output = read_smartctl.read_smartctl(filedir)

    assert output == expect
