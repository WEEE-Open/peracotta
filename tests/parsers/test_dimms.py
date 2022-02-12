#!/usr/bin/env python3

from parsers import read_decode_dimms
from tests.parsers.read_file import read_file

filedir = "tests/source_files/decode-dimms/"


def test_ecc_ram1():
    expect = [
        {
            "type": "ram",
            "working": "yes",
            "brand": "Kingston",
            "model": "K",
            "sn": "3375612524",
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
            "sn": "3392385900",
            "frequency-hertz": 667000000,
            "capacity-byte": 2147483648,
            "ram-type": "ddr2",
            "ram-ecc": "yes",
            "ram-timings": "5-5-5-15",
        },
    ]
    output = read_decode_dimms.parse_decode_dimms(
        read_file(filedir, "ECC/R451-R450.txt")
    )

    assert output == expect


def test_ecc_ram1_not_an_hex():
    expect = [
        {
            "type": "ram",
            "working": "yes",
            "brand": "Kingston",
            "model": "K",
            "sn": "0F00xb4r",
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
            "sn": "0xCA33B3RC",
            "frequency-hertz": 667000000,
            "capacity-byte": 2147483648,
            "ram-type": "ddr2",
            "ram-ecc": "yes",
            "ram-timings": "5-5-5-15",
        },
    ]
    output = read_decode_dimms.parse_decode_dimms(
        read_file(filedir, "ECC/R451-R450-notanhex.txt")
    )

    assert output == expect


def test_ecc_ram2():
    expect = [
        {
            "type": "ram",
            "working": "yes",
            "brand": "Kingston",
            "sn": "2853609420",
            "frequency-hertz": 667000000,
            "capacity-byte": 1073741824,
            "ram-type": "ddr2",
            "ram-ecc": "yes",
            "ram-timings": "5-5-5-15",
        },
        {
            "type": "ram",
            "working": "yes",
            "brand": "Kingston",
            "sn": "2836829644",
            "frequency-hertz": 667000000,
            "capacity-byte": 1073741824,
            "ram-type": "ddr2",
            "ram-ecc": "yes",
            "ram-timings": "5-5-5-15",
        },
    ]
    output = read_decode_dimms.parse_decode_dimms(
        read_file(filedir, "ECC/R480-R479.txt")
    )

    assert output == expect


def test_ram1():
    expect = [
        {
            "type": "ram",
            "working": "yes",
            "brand": "SK Hynix (former Hyundai Electronics)",
            "model": "HYMP112U64CP8-S6",
            "sn": "16416",
            "frequency-hertz": 800000000,
            "capacity-byte": 1073741824,
            "ram-type": "ddr2",
            "ram-ecc": "no",
            "ram-timings": "6-6-6-18",
        },
        {
            "type": "ram",
            "working": "yes",
            "brand": "SK Hynix (former Hyundai Electronics)",
            "model": "HYMP112U64CP8-S6",
            "sn": "8224",
            "frequency-hertz": 800000000,
            "capacity-byte": 1073741824,
            "ram-type": "ddr2",
            "ram-ecc": "no",
            "ram-timings": "6-6-6-18",
        },
        {
            "type": "ram",
            "working": "yes",
            "brand": "SK Hynix (former Hyundai Electronics)",
            "model": "HYMP112U64CP8-S6",
            "sn": "12320",
            "frequency-hertz": 800000000,
            "capacity-byte": 1073741824,
            "ram-type": "ddr2",
            "ram-ecc": "no",
            "ram-timings": "6-6-6-18",
        },
        {
            "type": "ram",
            "working": "yes",
            "brand": "SK Hynix (former Hyundai Electronics)",
            "model": "HYMP112U64CP8-S6",
            "sn": "8225",
            "frequency-hertz": 800000000,
            "capacity-byte": 1073741824,
            "ram-type": "ddr2",
            "ram-ecc": "no",
            "ram-timings": "6-6-6-18",
        },
    ]
    output = read_decode_dimms.parse_decode_dimms(
        read_file(filedir, "non ECC/R469-R470-R471-R472.txt")
    )

    assert output == expect
