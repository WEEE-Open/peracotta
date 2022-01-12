#!/usr/bin/env python3
import os

from parsers import read_smartctl
from parsers import read_decode_dimms
from parsers import read_dmidecode
from parsers import read_lspci_and_glxinfo
from parsers import read_lscpu

filedir = "tests/source_files/rottame/"


def test_lspci():
    expect = {
        "type": "graphics-card",
        "working": "yes",
        "brand": "ASUSTeK Computer Inc.",
        "model": "GeForce4 MX 440SE AGP 8x",
        "internal-name": "NV18",
        "capacity-byte": None,  # Missing glxinfo :(
        "brand-manufacturer": "Nvidia",
    }
    # False to ignore missing glxinfo
    output = read_lspci_and_glxinfo.read_lspci_and_glxinfo(
        False, os.path.join(filedir, "lspci.txt"), os.path.join(filedir, "glxinfo.txt")
    )

    assert output == expect


def test_lscpu():
    expect = {
        "type": "cpu",
        "working": "yes",
        "isa": "x86-64",
        "model": "Pentium D 2.66GHz",
        "brand": "Intel",
        "core-n": 2,
        "thread-n": 2,
        "frequency-hertz": 2660000000,
    }
    output = read_lscpu.read_lscpu(os.path.join(filedir, "lscpu.txt"))

    assert output == expect


def test_ram():
    expect = [
        {
            "type": "ram",
            "working": "yes",
            "brand": "Kingston",
            "model": "Undefined",
            "sn": "2972574626",
            "frequency-hertz": 533000000,
            "capacity-byte": 536870912,
            "ram-type": "ddr2",
            "ram-ecc": "no",
            "ram-timings": "5-4-4-12",
        }
    ]
    output = read_decode_dimms.read_decode_dimms(os.path.join(filedir, "dimms.txt"))

    assert output == expect


def test_baseboard():
    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASUSTeK Computer INC.",
        "model": "P5VDC-MX",
        "sn": "MB-1234567890",
    }
    output = read_dmidecode.get_baseboard(os.path.join(filedir, "baseboard.txt"))

    assert output == expect


def test_connector():
    baseboard = read_dmidecode.get_baseboard(os.path.join(filedir, "baseboard.txt"))

    expect = {
        "type": "motherboard",
        "working": "yes",
        "brand": "ASUSTeK Computer INC.",
        "model": "P5VDC-MX",
        "sn": "MB-1234567890",
        "ps2-ports-n": 2,
        "usb-ports-n": 8,
        "parallel-ports-n": 1,
        "serial-ports-n": 1,
        "vga-ports-n": 1,
        "mini-jack-ports-n": 3,
        "ethernet-ports-n": 1,
        "ide-ports-n": 2,
        "notes": "",
    }
    output = read_dmidecode.get_connectors(
        os.path.join(filedir, "connector.txt"), baseboard
    )

    assert output == expect


def test_chassis():
    # Generic Chassis is generic
    expect = {
        "type": "case",
        "brand": "Chassis Manufacture",
        "model": "",
        "sn": "Chassis Serial Number",
        "motherboard-form-factor": "",
    }
    output = read_dmidecode.get_chassis(os.path.join(filedir, "chassis.txt"))

    assert output == expect


def test_smartctl():
    expect = [
        {
            "type": "hdd",
            "brand": "Maxtor",
            "model": "6V080E0",
            "family": "DiamondMax 10 (SATA/300)",
            "sn": "V66666BG",
            "sata-ports-n": 1,
            "wwn": "0 150500 2ae42de3c",
            "spin-rate-rpm": -1,
            "capacity-decibyte": 82000000000,
            "smart-data": "ok",
            "notes": "Vendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAGS    VALUE WORST THRESH FAIL RAW_VALUE\n  3 Spin_Up_Time            POS--K   224   224   063    -    10393\n  4 Start_Stop_Count        -O--CK   253   253   000    -    591\n  5 Reallocated_Sector_Ct   PO--CK   253   253   063    -    0\n  7 Seek_Error_Rate         -O-R--   251   241   000    -    4\n  8 Seek_Time_Performance   POS--K   244   241   187    -    46094\n  9 Power_On_Hours          -O--CK   248   248   000    -    2002\n 10 Spin_Retry_Count        PO-R-K   253   252   157    -    0\n 11 Calibration_Retry_Count PO-R-K   253   252   223    -    0\n 12 Power_Cycle_Count       -O--CK   252   252   000    -    597\n189 High_Fly_Writes         -O-RCK   100   100   000    -    0\n190 Airflow_Temperature_Cel -O---K   067   052   000    -    33 (Min/Max 28/33)\n192 Power-Off_Retract_Count -O--CK   253   253   000    -    0\n193 Load_Cycle_Count        -O--CK   253   253   000    -    0\n194 Temperature_Celsius     -O--CK   038   253   000    -    33\n195 Hardware_ECC_Recovered  -O-R--   253   252   000    -    1026\n196 Reallocated_Event_Count ---R--   253   253   000    -    0\n197 Current_Pending_Sector  ---R--   253   253   000    -    0\n198 Offline_Uncorrectable   ---R--   253   253   000    -    0\n199 UDMA_CRC_Error_Count    ---R--   199   199   000    -    0\n200 Multi_Zone_Error_Rate   -O-R--   253   252   000    -    0\n201 Soft_Read_Error_Rate    -O-R--   253   252   000    -    2\n202 Data_Address_Mark_Errs  -O-R--   253   252   000    -    0\n203 Run_Out_Cancel          PO-R--   253   252   180    -    0\n204 Soft_ECC_Correction     -O-R--   253   252   000    -    0\n205 Thermal_Asperity_Rate   -O-R--   253   252   000    -    0\n207 Spin_High_Current       -O-R-K   253   252   000    -    0\n208 Spin_Buzz               -O-R-K   253   252   000    -    0\n210 Unknown_Attribute       -O--CK   253   252   000    -    0\n211 Unknown_Attribute       -O--CK   253   252   000    -    0\n212 Unknown_Attribute       -O--CK   253   252   000    -    0\n                            ||||||_ K auto-keep\n                            |||||__ C event count\n                            ||||___ R error rate\n                            |||____ S speed/performance\n                            ||_____ O updated online\n                            |______ P prefailure warning",
        }
    ]
    output = read_smartctl.read_smartctl(filedir)

    assert output == expect
