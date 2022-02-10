#!/usr/bin/env python3

from parsers import read_smartctl
from tests.parsers.read_file import read_file
import pytest

results = [
    ("test0.txt", [
        {
            'brand': 'Hitachi',
            'capacity-decibyte': 500000000000,
            'family': 'Travelstar 5K500.B',
            'hdd-form-factor': '2.5-7mm',
            'model': 'HTS545050B9A300',
            'sata-ports-n': 1,
            'smart-data': 'fail',
            'sn': '12345AEIOU123LOL456',
            'spin-rate-rpm': 5400,
            'type': 'hdd',
            'wwn': '5 3274 67846875936'
        }
    ]),
    ("test1.txt", [
        {
            'brand': 'Maxtor',
            'capacity-decibyte': 320000000000,
            'family': 'Maxtor DiamondMax 21',
            'model': 'STM3320820AS',
            'smart-data': 'ok',
            'sn': '9ABC12435',
            'type': 'hdd'
        }
    ]),
    ("test2.txt", [
        {'brand': 'Western Digital',
         'capacity-decibyte': 40000000000,
         'family': 'Caviar',
         'model': 'WD400BB-00DKA0',
         'smart-data': 'ok',
         'sn': 'WCAHM356436',
         'type': 'hdd'}
    ]),
     ("test3.txt", [
         {'brand': 'Seagate',
          'capacity-decibyte': 250000000000,
          'family': 'Barracuda 7200.10',
          'model': 'ST3250310AS',
          'smart-data': 'old',
          'sn': '9RY53ABC',
          'type': 'hdd'}
    ]),
    ("test4.txt", [
        {'brand': 'Western Digital',
         'capacity-decibyte': 160000000000,
         'family': 'Caviar SE Serial ATA',
         'model': 'WD1600JS-60MHB5',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': 'WCANM33344334',
         'type': 'hdd'}
    ]),
    ("test5.txt", [
        {'brand': 'Seagate',
         'capacity-decibyte': 1000000000000,
         'family': 'Desktop SSHD',
         'hdd-form-factor': '3.5',
         'model': 'ST1000DX001-1CM162',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': 'ZZZ12356',
         'spin-rate-rpm': 7200,
         'type': 'hdd',
         'wwn': '5 3152 546456464556'}
    ]),
    ("test6.txt", [
        {'brand': 'Western Digital',
         'capacity-decibyte': 320000000000,
         'family': 'Caviar Blue Serial ATA',
         'model': 'WD3200AAJS-00VWA0',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': 'WCARW3489748',
         'type': 'hdd',
         'wwn': '5 5358 7337373773'}
    ]),
    ("test7.txt", [
        {'brand': 'Western Digital',
         'capacity-decibyte': 40000000000,
         'family': 'Caviar',
         'model': 'WD400BB-60JKC0',
         'smart-data': 'ok',
         'sn': 'WCAMF97867543',
         'type': 'hdd'}
    ]),
    ("test8.txt", [
        {'capacity-decibyte': 128000000000,
         'hdd-form-factor': '2.5-7mm',
         'model': 'SSD128GBS800',
         'sata-ports-n': 1,  # This is mSATA and impossible to detect
         'smart-data': 'ok',
         'sn': 'AA000000000000000069',
         'type': 'ssd'}
    ]),
    ("test9.txt", [
        {'brand': 'Western Digital',
         'capacity-decibyte': 1000000000000,
         'm2-connectors-n': 1,
         'model': 'WDS100T2B0C-00PXH0',
         'sn': '91341V57464',
         'hdd-form-factor': 'm2',
         'type': 'ssd'}
    ]),
    ("test10.txt", [
        {'brand': 'Kingston',
         'capacity-decibyte': 480000000000,
         'family': 'Phison Driven SSDs',
         'model': 'SA400S37480G',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': '69696B12345678ABC',
         'type': 'ssd',
         'wwn': '5 9911 28933933'}
    ]),
    ("test11.txt", [
        {'capacity-decibyte': 960000000000,
         'm2-connectors-n': 1,
         'model': 'Force MP510',
         'sn': '1246751637284348D',
         'hdd-form-factor': 'm2',
         'type': 'ssd'}
    ]),
    ("test12.txt", [
        {'brand': 'Western Digital',
         'capacity-decibyte': 1000000000000,
         'm2-connectors-n': 1,
         'model': 'WDS100T2B0C-00PXH0',
         'sn': '3030ABCD4040EFG',
         'hdd-form-factor': 'm2',
         'type': 'ssd'}
    ]),
    ("test13.txt", [
        {'brand': 'Apple',
         'capacity-decibyte': 500000000000,
         'family': 'SD/SM/TS...E/F/G SSDs',
         'model': 'SM0512F',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': 'S1K3NYC123456',
         'type': 'ssd',
         'wwn': '5 9528 577455447'}
    ]),
    ("test14.txt", [
        {'brand': 'Kingston',
         'capacity-decibyte': 480000000000,
         'family': 'Phison Driven SSDs',
         'model': 'SA400S37480G',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': '35463B75353DCE1A3',
         'type': 'ssd',
         'wwn': '5 9911 34543545'}
    ]),
    ("test15.txt", [
        {'type': 'hdd'}
    ]),
    ("test16.txt", [
        {'brand': 'Kingston',
         'capacity-decibyte': 500000000000,
         'm2-connectors-n': 1,
         'hdd-form-factor': 'm2',
         'model': 'SNVS500G',
         'sn': '50026B7AB42CCC',
         'type': 'ssd'}
    ]),
    ("test17.txt", [
        {'capacity-decibyte': 480000000000,
         'hdd-form-factor': '2.5-7mm',
         'model': 'SATA3 480GB',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': '2021013101337',
         'type': 'ssd'}
    ]),
    ("test18.txt", [
        {'brand': 'Seagate',
         'capacity-decibyte': 1000000000000,
         'family': 'Barracuda Green (AF)',
         'model': 'ST1000DL002-9TT153',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': 'W17H45D',
         'spin-rate-rpm': 5900,
         'type': 'hdd',
         'wwn': '5 3152 2897212752'}
    ]),
    ("test19.txt", [
        {'capacity-decibyte': 120000000000,
         'hdd-form-factor': '2.5-7mm',
         'model': 'SATA3 120GB',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': '201012310234',
         'type': 'ssd'}
    ]),
    ("test20.txt", [
        {'capacity-decibyte': 120000000000,
         'hdd-form-factor': '2.5-7mm',
         'model': 'SATA3 120GB',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': '12345678990123',
         'type': 'ssd'}
    ]),
    ("test21.txt", [
        {'brand': 'Crucial/Micron',
         'capacity-decibyte': 480000000000,
         'family': 'Client SSDs',
         'hdd-form-factor': '2.5-7mm',
         'model': 'CT480BX500SSD1',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': '2022E666B444',
         'type': 'ssd',
         'wwn': '0 0 0'}
    ]),
    ("test22.txt", [
        {'brand': 'Kingston',
         'capacity-decibyte': 500000000000,
         'hdd-form-factor': 'm2',
         'm2-connectors-n': 1,
         'model': 'SNVS500G',
         'sn': '50027686CA6886AB',
         'type': 'ssd'}
    ]),
    ("test23.txt", [
        {'brand': 'Kingston',
         'capacity-decibyte': 240000000000,
         'family': 'Phison Driven SSDs',
         'model': 'SA400S37240G',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': '5002786787CECE78996',
         'type': 'ssd',
         'wwn': '5 9911 1111222223333'}
    ]),
    ("test24.txt", [
        {'brand': 'Adata',
         'capacity-decibyte': 240000000000,
         'family': 'Silicon Motion based SSDs',
         'hdd-form-factor': '2.5-7mm',
         'model': 'SU650',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': '2I098765432',
         'type': 'ssd',
         'wwn': '0 0 0'}
    ]),
]


@pytest.mark.parametrize("filename,expected", results)
def test_smartctl_single(filename, expected):
    filedir = "tests/source_files/smartctl/"
    output = read_smartctl.parse_smartctl(read_file(filedir, filename))

    assert output == expected


def test_smartctl_triple():
    expected = [
        {'brand': 'Western Digital',
         'capacity-decibyte': 40000000000,
         'family': 'Caviar',
         'model': 'WD400BB-00DKA0',
         'smart-data': 'ok',
         'sn': 'WCAHM786543',
         'type': 'hdd'},
        {'brand': 'Seagate',
         'capacity-decibyte': 1000000000000,
         'family': 'Desktop SSHD',
         'hdd-form-factor': '3.5',
         'model': 'ST1000DX001-1CM162',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': '45DL0LXD',
         'spin-rate-rpm': 7200,
         'type': 'hdd',
         'wwn': '5 3152 256262626'},
        {'brand': 'Western Digital',
         'capacity-decibyte': 160000000000,
         'family': 'Caviar SE Serial ATA',
         'model': 'WD1600JS-60MHB5',
         'sata-ports-n': 1,
         'smart-data': 'ok',
         'sn': 'WCANM89765430',
         'type': 'hdd'}
    ]

    filedir = "tests/source_files/smartctl/"
    output = read_smartctl.parse_smartctl(read_file(filedir, "three.txt"))

    assert len(output) == 3
    assert output == expected
