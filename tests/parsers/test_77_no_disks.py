#!/usr/bin/env python3

from peracotta.parsers import read_lscpu

from tests.parsers.read_file import read_file

filedir = "tests/source_files/77-no-disks/"


def test_lscpu():
    expect = [
        {
            "type": "cpu",
            "working": "yes",
            "isa": "x86-32",
            "model": "Celeron 2.80GHz",
            "brand": "Intel",
            "core-n": 1,
            "thread-n": 1,
            "frequency-hertz": 2800000000,
        }
    ]
    output = read_lscpu.parse_lscpu(read_file(filedir, "lscpu.txt"))

    assert output == expect
