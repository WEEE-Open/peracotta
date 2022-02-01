#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = "tests/source_files/travasato/"


def test_lspci():
    expect = {
        "type": "graphics-card",
        "working": "yes",
        "brand": "ASUSTeK Computer Inc.",
        "model": "GeForce GT 610",
        "internal-name": "GF119",
        "capacity-byte": None,  # Still no glxinfo :(
        "brand-manufacturer": "Nvidia",
    }
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        False, os.path.join(filedir, "lspci.txt"), os.path.join(filedir, "glxinfo.txt")
    )

    assert output == expect


def test_lscpu():
    expect = {
        "type": "cpu",
        "working": "yes",
        "isa": "x86-64",
        "model": "Core 2 Quad Q6600",
        "brand": "Intel",
        "core-n": 4,
        "thread-n": 4,
        "frequency-hertz": 2400000000,
    }
    output = read_lscpu.parse_lscpu(os.path.join(filedir, "lscpu.txt"))

    assert output == expect


def test_ram():
    expect = [
        {
            "type": "ram",
            "working": "yes",
            "brand": "Kingston",
            "model": "K",
            "sn": "3375612238",
            "frequency-hertz": 667000000,
            "capacity-byte": 2147483648,
            "ram-type": "ddr2",
            "ram-ecc": "yes",
            "ram-timings": "5-5-5-15",
        },
        {
            "type": "ram",
            "working": "yes",
            "brand": "Kingston",
            "model": "K",
            "sn": "3392385358",
            "frequency-hertz": 667000000,
            "capacity-byte": 2147483648,
            "ram-type": "ddr2",
            "ram-ecc": "yes",
            "ram-timings": "5-5-5-15",
        },
    ]
    output = read_decode_dimms.parse_decode_dimms(os.path.join(filedir, "dimms.txt"))

    assert output == expect


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Intel Corporation",
        "model": "D975XBX2",
        "sn": "BAOB4B9001YY",
    }
    output = read_dmidecode.get_baseboard(os.path.join(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "Intel Corporation",
        "model": "D975XBX2",
        "sn": "BAOB4B9001YY",
        "ide-ports-n": 2,
        "notes": "",
    }
    output = read_dmidecode.get_connectors(
        os.path.join(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_chassis():
    # At least it's not assuming stuff it cannot know...
    expect = {
        "type": "case",
        "brand": "",
        "model": "",
        "sn": "",
        "motherboard-form-factor": "",
    }
    output = read_dmidecode.parse_case(os.path.join(filedir, "chassis.txt"))

    assert output == expect


def test_smartctl():
    expect = [
        {
            "type": "hdd",
            "brand": "Hitachi",
            "model": "HDT725025VLA380",
            "family": "Deskstar T7K500",
            "wwn": "5 000cca 6904de32c",
            "sn": "VFA100R24D8ELK",
            "capacity-decibyte": 250000000000,
            "spin-rate-rpm": -1,
            "smart-data": "ok",
            "notes": "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     PO-R--   100   100   016    -    0\n  2 Throughput_Performance  P-S---   100   100   050    -    0\n  3 Spin_Up_Time            POS---   115   115   024    -    330 (Average 321)\n  4 Start_Stop_Count        -O--C-   100   100   000    -    89\n  5 Reallocated_Sector_Ct   PO--CK   100   100   005    -    4\n  7 Seek_Error_Rate         PO-R--   100   100   067    -    0\n  8 Seek_Time_Performance   P-S---   100   100   020    -    0\n  9 Power_On_Hours          -O--C-   090   090   000    -    74780\n 10 Spin_Retry_Count        PO--C-   100   100   060    -    0\n 12 Power_Cycle_Count       -O--CK   100   100   000    -    89\n192 Power-Off_Retract_Count -O--CK   098   098   000    -    3201\n193 Load_Cycle_Count        -O--C-   098   098   000    -    3201\n194 Temperature_Celsius     -O----   176   176   000    -    34 (Min/Max 14/56)\n196 Reallocated_Event_Count -O--CK   100   100   000    -    4\n197 Current_Pending_Sector  -O---K   100   100   000    -    0\n198 Offline_Uncorrectable   ---R--   100   100   000    -    0\n199 UDMA_CRC_Error_Count    -O-R--   200   253   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning",
        }
    ]
    output = read_smartctl.read_smartctl(filedir)

    assert output == expect
