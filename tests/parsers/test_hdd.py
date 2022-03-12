#!/usr/bin/env python3

from parsers import read_smartctl
from tests.parsers.read_file import read_file
import pytest


results = [
    (
        "test0.txt",
        [
            {
                "brand": "Hitachi",
                "capacity-decibyte": 500000000000,
                "family": "Travelstar 5K500.B",
                "hdd-form-factor": "2.5",
                "height-mm": 9.5,
                "model": "HTS545050B9A300",
                "sata-ports-n": 1,
                "smart-data": "fail",
                "sn": "12345AEIOU123LOL456",
                "spin-rate-rpm": 5400,
                "type": "hdd",
                "wwn": "5 3274 67846875936",
            }
        ],
    ),
    (
        "test1.txt",
        [
            {
                "brand": "Maxtor",
                "capacity-decibyte": 320000000000,
                "family": "Maxtor DiamondMax 21",
                "hdd-form-factor": "3.5",
                "model": "STM3320820AS",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "9ABC12435",
                "type": "hdd",
            }
        ],
    ),
    (
        "test2.txt",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 40000000000,
                "family": "Caviar",
                "model": "WD400BB-00DKA0",
                "smart-data": "ok",
                "spin-rate-rpm": 7200,
                "ide-ports-n": 1,
                "sn": "WCAHM356436",
                "type": "hdd",
            }
        ],
    ),
    (
        "test3.txt",
        [
            {
                "brand": "Seagate",
                "capacity-decibyte": 250000000000,
                "family": "Barracuda 7200.10",
                "hdd-form-factor": "3.5",
                "model": "ST3250310AS",
                "sata-ports-n": 1,
                "smart-data": "old",
                "sn": "9RY53ABC",
                "spin-rate-rpm": 7200,
                "type": "hdd",
            }
        ],
    ),
    (
        "test4.txt",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 160000000000,
                "family": "Caviar SE",
                "model": "WD1600JS-60MHB5",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "spin-rate-rpm": 7200,
                "sn": "WCANM33344334",
                "type": "hdd",
            }
        ],
    ),
    (
        "test5.txt",
        [
            {
                "brand": "Seagate",
                "capacity-decibyte": 1000000000000,
                "family": "Desktop SSHD",
                "hdd-form-factor": "3.5",
                "model": "ST1000DX001-1CM162",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "ZZZ12356",
                "spin-rate-rpm": 7200,
                "type": "hdd",
                "wwn": "5 3152 546456464556",
            }
        ],
    ),
    (
        "test6.txt",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 320000000000,
                "family": "Caviar Blue",
                "hdd-form-factor": "3.5",
                "model": "WD3200AAJS-00VWA0",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "WCARW3489748",
                "spin-rate-rpm": 7200,
                "type": "hdd",
                "wwn": "5 5358 7337373773",
            }
        ],
    ),
    (
        "test7.txt",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 40000000000,
                "family": "Caviar",
                "model": "WD400BB-60JKC0",
                "smart-data": "ok",
                "spin-rate-rpm": 7200,
                "ide-ports-n": 1,
                "sn": "WCAMF97867543",
                "type": "hdd",
            }
        ],
    ),
    (
        "test8.txt",
        [
            {
                "capacity-decibyte": 128000000000,
                "hdd-form-factor": "2.5",
                "model": "SSD128GBS800",
                "sata-ports-n": 1,  # This is mSATA and impossible to detect
                "smart-data": "ok",
                "sn": "AA000000000000000069",
                "type": "ssd",
            }
        ],
    ),
    (
        "test9.txt",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 1000000000000,
                "m2-connectors-n": 1,
                "model": "WDS100T2B0C-00PXH0",
                "sn": "91341V57464",
                "hdd-form-factor": "m2",
                "type": "ssd",
            }
        ],
    ),
    (
        "test10.txt",
        [
            {
                "brand": "Kingston",
                "capacity-decibyte": 480000000000,
                "family": "Phison Driven SSDs",
                "model": "SA400S37480G",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "69696B12345678ABC",
                "type": "ssd",
                "wwn": "5 9911 28933933",
            }
        ],
    ),
    (
        "test11.txt",
        [{"capacity-decibyte": 960000000000, "m2-connectors-n": 1, "model": "Force MP510", "sn": "1246751637284348D", "hdd-form-factor": "m2", "type": "ssd"}],
    ),
    (
        "test12.txt",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 1000000000000,
                "m2-connectors-n": 1,
                "model": "WDS100T2B0C-00PXH0",
                "sn": "3030ABCD4040EFG",
                "hdd-form-factor": "m2",
                "type": "ssd",
            }
        ],
    ),
    (
        "test13.txt",
        [
            {
                "brand": "Apple",
                "capacity-decibyte": 500000000000,
                "family": "SD/SM/TS...E/F/G SSDs",
                "model": "SM0512F",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "S1K3NYC123456",
                "type": "ssd",
                "wwn": "5 9528 577455447",
            }
        ],
    ),
    (
        "test14.txt",
        [
            {
                "brand": "Kingston",
                "capacity-decibyte": 480000000000,
                "family": "Phison Driven SSDs",
                "model": "SA400S37480G",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "35463B75353DCE1A3",
                "type": "ssd",
                "wwn": "5 9911 34543545",
            }
        ],
    ),
    ("test15.txt", [{"type": "hdd"}]),
    (
        "test16.txt",
        [
            {
                "brand": "Kingston",
                "capacity-decibyte": 500000000000,
                "m2-connectors-n": 1,
                "hdd-form-factor": "m2",
                "model": "SNVS500G",
                "sn": "50026B7AB42CCC",
                "type": "ssd",
            }
        ],
    ),
    (
        "test17.txt",
        [
            {
                "capacity-decibyte": 480000000000,
                "hdd-form-factor": "2.5",
                "model": "SATA3 480GB",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "2021013101337",
                "type": "ssd",
            }
        ],
    ),
    (
        "test18.txt",
        [
            {
                "brand": "Seagate",
                "capacity-decibyte": 1000000000000,
                "family": "Barracuda Green (AF)",
                "model": "ST1000DL002-9TT153",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "W17H45D",
                "spin-rate-rpm": 5900,
                "type": "hdd",
                "wwn": "5 3152 2897212752",
            }
        ],
    ),
    (
        "test19.txt",
        [
            {
                "capacity-decibyte": 120000000000,
                "hdd-form-factor": "2.5",
                "model": "SATA3 120GB",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "201012310234",
                "type": "ssd",
            }
        ],
    ),
    (
        "test20.txt",
        [
            {
                "capacity-decibyte": 120000000000,
                "hdd-form-factor": "2.5",
                "model": "SATA3 120GB",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "12345678990123",
                "type": "ssd",
            }
        ],
    ),
    (
        "test21.txt",
        [
            {
                "brand": "Crucial/Micron",
                "capacity-decibyte": 480000000000,
                "family": "Client SSDs",
                "hdd-form-factor": "2.5",
                "model": "CT480BX500SSD1",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "2022E666B444",
                "type": "ssd",
                "wwn": "0 0 0",
            }
        ],
    ),
    (
        "test22.txt",
        [
            {
                "brand": "Kingston",
                "capacity-decibyte": 500000000000,
                "hdd-form-factor": "m2",
                "m2-connectors-n": 1,
                "model": "SNVS500G",
                "sn": "50027686CA6886AB",
                "type": "ssd",
            }
        ],
    ),
    (
        "test23.txt",
        [
            {
                "brand": "Kingston",
                "capacity-decibyte": 240000000000,
                "family": "Phison Driven SSDs",
                "model": "SA400S37240G",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "5002786787CECE78996",
                "type": "ssd",
                "wwn": "5 9911 1111222223333",
            }
        ],
    ),
    (
        "test24.txt",
        [
            {
                "brand": "Adata",
                "capacity-decibyte": 240000000000,
                "family": "Silicon Motion based SSDs",
                "hdd-form-factor": "2.5",
                "model": "SU650",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "2I098765432",
                "type": "ssd",
                "wwn": "0 0 0",
            }
        ],
    ),
    (
        "test25.txt",
        [
            {
                "brand": "Sun",
                "capacity-decibyte": 73300000000,
                "model": "Linux",
                "notes": "This is a SCSI disk, however it is not possible to detect the " "exact connector type. Please set the correct one manually.",
                "sn": "BAEBAE123",
                "type": "ssd",
            }
        ],
    ),
    (
        "test26.txt",
        [
            {
                "brand": "Samsung",
                "capacity-decibyte": 250000000000,
                "model": "840 EVO 250GB",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "C140N333333",
                "type": "ssd",
                "wwn": "5 9528 9876543274",
            }
        ],
    ),
    (
        "ide01.json",
        [
            {
                "brand": "Samsung",
                "capacity-decibyte": 20400000000,
                "model": "SV2042H",
                "ide-ports-n": 1,
                "smart-data": "fail",
                "sn": "REDACTED123456",
                "type": "hdd",
            }
        ],
    ),
    (
        "ide02.json",
        [
            {
                "brand": "Hitachi",
                "capacity-decibyte": 160000000000,
                "family": "Deskstar P7K500",
                "hdd-form-factor": "3.5",
                "model": "HDP725016GLAT80",
                "ide-ports-n": 1,
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
                "wwn": "5 3274 123456789",
            }
        ],
    ),
    (
        "ide03.json",
        [
            {
                "brand": "Quantum",
                "capacity-decibyte": 13000000000,
                "family": "Fireball CR",
                "model": "FIREBALL CR13.0A",
                "ide-ports-n": 1,
                "smart-data": "old",
                "sn": "REDACTED123456",
                "type": "hdd",
            }
        ],
    ),
    (
        "ide04.json",
        [
            {
                "brand": "Quantum",
                "capacity-decibyte": 20400000000,
                "model": "FIREBALL CX20.4A",
                "ide-ports-n": 1,
                "sn": "REDACTED123456",
                "type": "hdd",
            }
        ],
    ),
    (
        "ide05.json",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 40000000000,
                "family": "Caviar",
                "model": "WD400BB-55JHA0",
                "ide-ports-n": 1,
                "smart-data": "ok",
                "spin-rate-rpm": 7200,
                "sn": "REDACTED123456",
                "type": "hdd",
            }
        ],
    ),
    (
        "ide06.json",
        [
            {
                "brand": "Maxtor",
                "capacity-decibyte": 164000000000,
                "family": "DiamondMax 10",
                "hdd-form-factor": "3.5",
                "model": "6L160P0",
                "ide-ports-n": 1,
                "smart-data": "fail",
                "sn": "REDACTED123456",
                "type": "hdd",
            }
        ],
    ),
    (
        "ide07.json",
        [
            {
                "type": "hdd",
            }
        ],
    ),
    (
        "ide08.json",
        [
            {
                "brand": "Maxtor",
                "capacity-decibyte": 40000000000,
                "family": "DiamondMax Plus D740X",
                "hdd-form-factor": "3.5",
                "model": "6L040J2",
                "ide-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "type": "hdd",
            }
        ],
    ),
    (
        "ide09.json",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 40000000000,
                "family": "Caviar",
                "model": "WD400BB-55JHA0",
                "smart-data": "ok",
                "spin-rate-rpm": 7200,
                "ide-ports-n": 1,
                "sn": "REDACTED123456",
                "type": "hdd",
            }
        ],
    ),
    (
        "mini_ide01.json",
        [
            {
                "brand": "Toshiba",
                "capacity-decibyte": 12100000000,
                "hdd-form-factor": "2.5",
                "mini-ide-ports-n": 1,
                "model": "MK1214GAP",
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 4200,
                "type": "hdd",
            }
        ],
    ),
    (
        "mini_ide02.json",
        [
            {
                "brand": "Hitachi",
                "capacity-decibyte": 60000000000,
                "family": "Travelstar 80GN",
                "hdd-form-factor": "2.5",
                "height-mm": 9.5,
                "model": "IC25N060ATMR04-0",
                "mini-ide-ports-n": 1,
                "smart-data": "fail",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 4200,
                "type": "hdd",
            }
        ],
    ),
    (
        "mini_ide03.json",
        [
            {
                "brand": "Fujitsu",
                "capacity-decibyte": 60000000000,
                "family": "MHV",
                "hdd-form-factor": "2.5",
                "model": "MHV2060AT PL",
                "mini-ide-ports-n": 1,
                "smart-data": "fail",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 4200,
                "type": "hdd",
            }
        ],
    ),
    (
        "mini_ide04.json",
        [
            {
                "brand": "Fujitsu",
                "capacity-decibyte": 40000000000,
                "family": "MHS AT",
                "hdd-form-factor": "2.5",
                "model": "MHS2040AT  D",
                "mini-ide-ports-n": 1,
                "smart-data": "sus",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 4200,
                "type": "hdd",
            }
        ],
    ),
    (
        "mini_ide05.json",
        [
            {
                "brand": "Fujitsu",
                "capacity-decibyte": 60000000000,
                "family": "MHT",
                "hdd-form-factor": "2.5",
                "model": "MHT2060AT PL",
                "mini-ide-ports-n": 1,
                "smart-data": "fail",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 4200,
                "type": "hdd",
            }
        ],
    ),
    (
        "mini_sata01.json",
        [
            {
                "brand": "Hitachi",
                "capacity-decibyte": 160000000000,
                "family": "Travelstar 5K250",
                "hdd-form-factor": "2.5",
                "height-mm": 9.5,
                "model": "HTS542516K9SA00",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 5400,
                "type": "hdd",
                "wwn": "5 3274 123456789",
            }
        ],
    ),
    (
        "mini_sata02.json",
        [
            {
                "brand": "Hitachi",
                "capacity-decibyte": 160000000000,
                "family": "Travelstar 5K250",
                "hdd-form-factor": "2.5",
                "height-mm": 9.5,
                "model": "HTS542516K9SA00",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 5400,
                "type": "hdd",
                "wwn": "5 3274 123456789",
            }
        ],
    ),
    (
        "mini_sata03.json",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 160000000000,
                "family": "Scorpio Blue",
                "hdd-form-factor": "2.5",
                "model": "WD1600BEVS-22RST0",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 5400,
                "type": "hdd",
                "wwn": "5 5358 123456789",
            }
        ],
    ),
    (
        "mini_sata04.json",
        [
            {
                "brand": "Toshiba",
                "capacity-decibyte": 320000000000,
                "family": "2.5\" HDD MK..75GSX",
                "hdd-form-factor": "2.5",
                "height-mm": 9.5,
                "model": "MK3275GSX",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 5400,
                "type": "hdd",
                "wwn": "5 57 123456789",
            }
        ],
    ),
    (
        "mini_sata05.json",
        [
            {
                # TODO: decode more data
                "brand": "Samsung",
                "capacity-decibyte": 160000000000,
                "family": "SpinPoint M5",
                # "hdd-form-factor": "2.5",
                "model": "HM160HI",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                # "spin-rate-rpm": 5400,
                "type": "hdd",
                "wwn": "5 983040 123456789",
            }
        ],
    ),
    (
        "mini_sata06.json",
        [
            {
                "brand": "Hitachi",
                "brand-manufacturer": "HGST",
                "capacity-decibyte": 320000000000,
                "family": "HGST Travelstar Z7K500",
                "hdd-form-factor": "2.5",
                "height-mm": 7,
                "model": "HTS725032A7E630",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
                "wwn": "5 3274 123456789",
            }
        ],
    ),
    (
        "mini_sata07.json",
        [
            {
                "brand": "Fujitsu",
                "capacity-decibyte": 250000000000,
                "family": "MHY BH",
                "hdd-form-factor": "2.5",
                "model": "MHY2250BH",
                "sata-ports-n": 1,
                "smart-data": "fail",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 5400,
                "type": "hdd",
                "wwn": "5 14 123456789",
            }
        ],
    ),
    (
        "mini_sata08.json",
        [
            {
                "brand": "Hitachi",
                "capacity-decibyte": 250000000000,
                "family": "Travelstar 5K250",
                "hdd-form-factor": "2.5",
                "height-mm": 9.5,
                "model": "HTS542525K9SA00",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 5400,
                "type": "hdd",
                "wwn": "5 3274 123456789",
            }
        ],
    ),
    (
        "mini_sata09.json",
        [
            {
                "brand": "Seagate",
                "capacity-decibyte": 320000000000,
                "family": "Momentus 5400.5",
                "hdd-form-factor": "2.5",
                "model": "ST9320320AS",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 5400,
                "type": "hdd",
                "wwn": "5 3152 123456789",
            }
        ],
    ),
    (
        "sata01.json",
        [
            {
                "brand": "Samsung",
                "capacity-decibyte": 160000000000,
                # "family": "",
                # "hdd-form-factor": "3.5",
                "model": "HD161HJ",
                # "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                # "spin-rate-rpm": 0,
                "type": "hdd",
                "wwn": "5 240 123456789",
            }
        ],
    ),
    (
        "sata02.json",
        [
            {
                "brand": "Seagate",
                "capacity-decibyte": 160000000000,
                "family": "Barracuda 7200.9",
                "hdd-form-factor": "3.5",
                "model": "ST3160812AS",
                "sata-ports-n": 1,
                "smart-data": "old",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
            }
        ],
    ),
    (
        "sata03.json",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 500000000000,
                "family": "Caviar Blue",
                "hdd-form-factor": "3.5",
                "model": "WD5000AAKS-00UU3A0",
                "sata-ports-n": 1,
                "smart-data": "fail",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
                "wwn": "5 5358 123456789",
            }
        ],
    ),
    (
        "sata04.json",
        [
            {
                "brand": "Seagate",
                "capacity-decibyte": 250000000000,
                "family": "Barracuda 7200.10",
                "hdd-form-factor": "3.5",
                "model": "ST3250310AS",
                "sata-ports-n": 1,
                "smart-data": "old",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
            }
        ],
    ),
    (
        "sata05.json",
        [
            {
                "brand": "Maxtor",
                "capacity-decibyte": 250000000000,
                "family": "Maxtor DiamondMax 21",
                "hdd-form-factor": "3.5",
                "model": "STM3250820AS",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                # "spin-rate-rpm": 0,
                "type": "hdd",
            }
        ],
    ),
    (
        "sata06.json",
        [
            {
                "brand": "Samsung",
                "capacity-decibyte": 160000000000,
                # "hdd-form-factor": "3.5",
                "model": "HD161HJ",
                # "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                # "spin-rate-rpm": 0,
                "type": "hdd",
                "wwn": "5 240 123456789",
            }
        ],
    ),
    (
        "sata07.json",
        [
            {
                "brand": "Samsung",
                "capacity-decibyte": 160000000000,
                # "hdd-form-factor": "3.5",
                "model": "HD161HJ",
                # "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                # "spin-rate-rpm": 0,
                "type": "hdd",
                "wwn": "5 240 123456789",
            }
        ],
    ),
    (
        "sata08.json",
        [
            {
                "brand": "Maxtor",
                "capacity-decibyte": 320000000000,
                "family": "Maxtor DiamondMax 21",
                "hdd-form-factor": "3.5",
                "model": "STM3320820AS",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                # "spin-rate-rpm": 0,
                "type": "hdd",
            }
        ],
    ),
    (
        "sata09.json",
        [
            {
                "brand": "Seagate",
                "capacity-decibyte": 80000000000,
                "family": "Barracuda 7200.10",
                "hdd-form-factor": "3.5",
                "model": "ST380815AS",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
            }
        ],
    ),
    (
        "sata10.json",
        [
            {
                "brand": "Hitachi",
                "capacity-decibyte": 500000000000,
                "family": "Deskstar T7K500",
                "hdd-form-factor": "3.5",
                "model": "HDT725050VLA360",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
                "wwn": "5 3274 123456789",
            }
        ],
    ),
    (
        "sata11.json",
        [
            {
                "brand": "Samsung",
                "capacity-decibyte": 160000000000,
                # "hdd-form-factor": "3.5",
                "model": "HD161HJ",
                # "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                # "spin-rate-rpm": 0,
                "type": "hdd",
                "wwn": "5 240 123456789",
            }
        ],
    ),
    (
        "sata12.json",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 500000000000,
                "family": "Blue",
                "hdd-form-factor": "3.5",
                "model": "WD5000AZLX-08K2TA0",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
                "wwn": "5 5358 123456789",
            }
        ],
    ),
    (
        "sata13.json",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 500000000000,
                "family": "Caviar Blue",
                "hdd-form-factor": "3.5",
                "model": "WD5000AAKS-00A7B0",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
                "wwn": "5 5358 123456789",
            }
        ],
    ),
    (
        "sata14.json",
        [
            {
                "brand": "Samsung",
                "capacity-decibyte": 160000000000,
                # "hdd-form-factor": "3.5",
                "model": "HD161HJ",
                # "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                # "spin-rate-rpm": 0,
                "type": "hdd",
                "wwn": "5 240 123456789",
            }
        ],
    ),
    (
        "sata15.json",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 500000000000,
                "family": "Caviar Black",
                "hdd-form-factor": "3.5",
                "model": "WD5003AZEX-00RLFA0",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
                "wwn": "5 5358 123456789",
            }
        ],
    ),
    (
        "sata16.json",
        [
            {
                "brand": "Seagate",
                "capacity-decibyte": 250000000000,
                "family": "Momentus 5400.5",
                "hdd-form-factor": "2.5",
                "model": "ST9250320AS",
                "sata-ports-n": 1,
                "smart-data": "ok",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 5400,
                "type": "hdd",
                "wwn": "5 3152 123456789",
            }
        ],
    ),
    (
        "smart_disabled.txt",
        [
            {
                "brand": "Western Digital",
                "capacity-decibyte": 40000000000,
                "family": "Caviar",
                "ide-ports-n": 1,
                "model": "WD400BB-00DKA0",
                "sn": "REDACTED123456",
                "spin-rate-rpm": 7200,
                "type": "hdd",
            }
        ],
    ),
]


@pytest.mark.smartctl
@pytest.mark.parametrize("filename,expected", results)
def test_smartctl_single(filename, expected):
    filedir = "tests/source_files/smartctl/"
    output = read_smartctl.parse_smartctl(read_file(filedir, filename))

    assert output == expected


@pytest.mark.smartctl
def test_smartctl_triple():
    expected = [
        {
            "brand": "Western Digital",
            "capacity-decibyte": 40000000000,
            "family": "Caviar",
            "model": "WD400BB-00DKA0",
            "smart-data": "ok",
            "sn": "WCAHM786543",
            "spin-rate-rpm": 7200,
            "ide-ports-n": 1,
            "type": "hdd",
        },
        {
            "brand": "Seagate",
            "capacity-decibyte": 1000000000000,
            "family": "Desktop SSHD",
            "hdd-form-factor": "3.5",
            "model": "ST1000DX001-1CM162",
            "sata-ports-n": 1,
            "smart-data": "ok",
            "sn": "45DL0LXD",
            "spin-rate-rpm": 7200,
            "type": "hdd",
            "wwn": "5 3152 256262626",
        },
        {
            "brand": "Western Digital",
            "capacity-decibyte": 160000000000,
            "family": "Caviar SE",
            "model": "WD1600JS-60MHB5",
            "sata-ports-n": 1,
            "smart-data": "ok",
            "spin-rate-rpm": 7200,
            "sn": "WCANM89765430",
            "type": "hdd",
        },
    ]

    filedir = "tests/source_files/smartctl/"
    output = read_smartctl.parse_smartctl(read_file(filedir, "three.txt"))

    assert len(output) == 3
    assert output == expected


@pytest.mark.smartctl
def test_smartctl_virtual_scsi():
    expected = [
        {
            "brand": "Msft",
            "capacity-decibyte": 275000000000,
            "model": "Virtual Disk",
            "notes": "This is a SCSI disk, however it is not possible to detect the " "exact connector type. Please set the correct one manually.",
            "type": "ssd",
        },
        {
            "brand": "Msft",
            "capacity-decibyte": 275000000000,
            "model": "Virtual Disk",
            "notes": "This is a SCSI disk, however it is not possible to detect the " "exact connector type. Please set the correct one manually.",
            "type": "ssd",
        },
    ]

    filedir = "tests/source_files/smartctl/"
    output = read_smartctl.parse_smartctl(read_file(filedir, "virtual_scsi.txt"))

    assert len(output) == 2
    assert output == expected
