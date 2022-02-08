#!/usr/bin/env python3

from parsers import read_smartctl
from tests.parsers.read_file import read_file

filedir = "tests/source_files/hdd/"


def test_smartctl():
    expect = [
        {
            "type": "hdd",
            "brand": "Toshiba",
            "model": "MQ01ABF050",
            "family": '2.5" HDD MQ01ABF...',
            "sn": "76H3EUCL",
            "sata-ports-n": 1,
            "wwn": "5 000039 7222954ce",
            "capacity-decibyte": 500000000000,
            "spin-rate-rpm": 5400,
            "smart-data": "ok",
            "hdd-form-factor": "2.5-7mm",
        }
    ]
    output = read_smartctl.parse_smartctl(read_file(filedir, "smartctl.txt"))

    assert output == expect
