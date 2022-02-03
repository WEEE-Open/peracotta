#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = "tests/source_files/asdpc2/"


def test_lspci():
    expect = {
        "type": "graphics-card",
        "working": "yes",
        "brand-manufacturer": "Intel",
        "brand": "ASUSTeK Computer Inc.",
        "internal-name": "",
        "model": "HD Graphics 515",
        "capacity-byte": None,
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
        "model": "Core m3-6Y30",
        "brand": "Intel",
        "core-n": 2,
        "thread-n": 4,
        "frequency-hertz": 900000000,
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
        "brand": "ASUSTeK COMPUTER INC.",
        "model": "UX305CA",
        "sn": "BSN12345678901234567",
    }
    output = read_dmidecode._get_baseboard(os.path.join(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode._get_baseboard(os.path.join(filedir, "baseboard.txt"))

    # Yep, the connector thing is empty...
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASUSTeK COMPUTER INC.",
        "model": "UX305CA",
        "sn": "BSN12345678901234567",
        "notes": "",
    }
    output = read_dmidecode._get_connectors(
        os.path.join(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_chassis():
    expect = {
        "type": "case",
        "brand": "ASUSTeK COMPUTER INC.",
        "model": "",
        "sn": "G6M0DF00361708D",
        "motherboard-form-factor": "proprietary-laptop",
    }
    output = read_dmidecode.parse_case(os.path.join(filedir, "chassis.txt"))

    assert output == expect


def test_smartctl():
    expect = [
        {
            "type": "ssd",
            "brand": "LiteOn",
            "model": "CV1-8B128",  # This is too much part of the model to extract
            "family": "",
            "sn": "CV1-8B128_006923456A",
            "wwn": "5 002303 234ddcce5",
            "capacity-byte": 128000000000,
            "smart-data": "ok",
            "sata-ports-n": 1,  # TODO: this is wrong, this is M.2
            "notes": "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  1 Raw_Read_Error_Rate     POSR-K   100   100   000    -    0\n  5 Reallocated_Sector_Ct   PO----   100   100   000    -    0\n  9 Power_On_Hours          -O----   100   100   000    -    5\n 12 Power_Cycle_Count       PO----   100   100   000    -    1735\n170 Unknown_Attribute       -O--CK   100   100   000    -    0\n171 Unknown_Attribute       PO----   100   100   000    -    0\n172 Unknown_Attribute       PO----   100   100   000    -    0\n173 Unknown_Attribute       PO----   100   100   000    -    22\n174 Unknown_Attribute       PO----   100   100   000    -    31\n175 Program_Fail_Count_Chip PO----   100   100   000    -    0\n176 Erase_Fail_Count_Chip   PO----   100   100   000    -    0\n177 Wear_Leveling_Count     PO----   100   100   000    -    22\n178 Used_Rsvd_Blk_Cnt_Chip  PO----   100   100   000    -    0\n179 Used_Rsvd_Blk_Cnt_Tot   PO----   100   100   000    -    0\n180 Unused_Rsvd_Blk_Cnt_Tot PO--CK   100   100   000    -    143\n181 Program_Fail_Cnt_Total  PO----   100   100   000    -    0\n182 Erase_Fail_Count_Total  PO----   100   100   000    -    0\n183 Runtime_Bad_Block       -O--CK   100   100   000    -    0\n189 Unknown_SSD_Attribute   ------   100   100   000    -    93\n191 Unknown_SSD_Attribute   ------   100   100   000    -    3\n192 Power-Off_Retract_Count PO----   100   100   000    -    31\n194 Temperature_Celsius     -O----   100   100   000    -    45\n195 Hardware_ECC_Recovered  PO----   100   100   000    -    0\n199 UDMA_CRC_Error_Count    PO----   100   100   000    -    0\n232 Available_Reservd_Space PO----   100   100   010    -    100\n233 Media_Wearout_Indicator PO----   100   100   000    -    88140\n241 Total_LBAs_Written      PO----   100   100   000    -    69582\n242 Total_LBAs_Read         PO----   100   100   000    -    31505\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning",
        }
    ]
    output = read_smartctl.read_smartctl(filedir)

    assert output == expect
