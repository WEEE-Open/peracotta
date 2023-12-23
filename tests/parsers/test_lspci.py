#!/usr/bin/env python3
import os

from peracotta.parsers import read_lspci_and_glxinfo
from tests.parsers.read_file import read_file

filedir = "tests/source_files/glxinfo+lspci/"


def test_lspci_dedicated1():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ASUSTeK Computer Inc.",
            "internal-name": "NV44",
            "model": "GeForce 6200 SE TurboCache",
            "capacity-byte": 67108864,  # 64 MB
            "brand-manufacturer": "Nvidia",
        }
    ]

    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        True,
        os.path.join(read_file(filedir, "dedicated/NVIDIA6200/lspci.txt")),
        os.path.join(read_file(filedir, "dedicated/NVIDIA6200/glxinfo.txt")),
    )

    assert output == expect


def test_lspci_dedicated2():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ASUSTeK Computer Inc.",
            "internal-name": "G96",
            "model": "GeForce 9400 GT",
            "capacity-byte": 1073741824,
            "brand-manufacturer": "Nvidia",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        True,
        read_file(filedir, "dedicated/lspci-9400GT.txt"),
        read_file(filedir, "dedicated/glxinfo-9400GT.txt"),
    )

    assert output == expect


def test_lspci_dedicated3():
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ASUSTeK Computer Inc.",
            "internal-name": "GM204",
            "model": "GeForce GTX 970",
            "capacity-byte": 4294967296,
            "brand-manufacturer": "Nvidia",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        True,
        read_file(filedir, "dedicated/lspci-gtx-970.txt"),
        read_file(filedir, "dedicated/glxinfo-gtx-970.txt"),
    )

    assert output == expect


def test_lspci_integrated_mobo_1():
    filesubdir = "integrated/on-mobo/"
    file = "8300GT"

    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ASUSTeK Computer Inc.",
            "model": "GeForce 8300",
            "internal-name": "C77",
            "brand-manufacturer": "Nvidia",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        False,
        os.path.join(read_file(filedir, f"{filesubdir}/lspci-{file}.txt")),
        os.path.join(read_file(filedir, f"{filesubdir}/glxinfo-{file}.txt")),
    )

    assert output == expect


def test_lspci_integrated_mobo_2():
    filesubdir = "integrated/on-mobo/"
    file = "82865G"

    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "Lite-On Technology Corporation",
            "model": "82865G",
            "brand-manufacturer": "Intel",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        False,
        os.path.join(read_file(filedir, f"{filesubdir}/lspci-{file}.txt")),
        os.path.join(read_file(filedir, f"{filesubdir}/glxinfo-{file}.txt")),
    )

    assert output == expect


def test_lspci_integrated_mobo_3():
    filesubdir = "integrated/on-mobo/"
    file = "ES1000"

    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "Intel Corporation",
            "model": "ES1000",
            "brand-manufacturer": "AMD/ATI",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        False,
        os.path.join(read_file(filedir, f"{filesubdir}/lspci-{file}.txt")),
        os.path.join(read_file(filedir, f"{filesubdir}/glxinfo-{file}.txt")),
    )

    assert output == expect


def test_lspci_integrated_cpu_1():
    filesubdir = "integrated/on-cpu/Acer Swift 3/"

    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "Acer Incorporated",
            "model": "Skylake GT2 [HD Graphics 520]",
            "brand-manufacturer": "Intel",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        False,
        os.path.join(read_file(filedir, f"{filesubdir}/lspci.txt")),
        os.path.join(read_file(filedir, f"{filesubdir}/glxinfo.txt")),
    )

    assert output == expect


def test_lspci_integrated_cpu_2():
    filesubdir = "integrated/on-cpu/HP EliteBook 2540p (i5 M540)/"

    # Yeeeeah, nice and detailed - not.
    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "Hewlett-Packard Company Core Processor",
            "brand-manufacturer": "Intel",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        False,
        os.path.join(read_file(filedir, f"{filesubdir}/lspci.txt")),
        os.path.join(read_file(filedir, f"{filesubdir}/glxinfo.txt")),
    )

    assert output == expect


def test_lspci_integrated_cpu_3():
    filesubdir = "integrated/on-cpu/Xeon/"

    expect = [
        {
            "type": "graphics-card",
            "working": "yes",
            "brand": "ASRock Incorporation",
            "model": "Xeon E3-1200 v3/4th Gen Core Processor",
            "brand-manufacturer": "Intel",
        }
    ]
    output = read_lspci_and_glxinfo.parse_lspci_and_glxinfo(
        False,
        os.path.join(read_file(filedir, f"{filesubdir}/lspci.txt")),
        os.path.join(read_file(filedir, f"{filesubdir}/glxinfo.txt")),
    )

    assert output == expect
