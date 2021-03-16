import prettyprinter
import pytest


def test_frequency():
	values = {
		100: "100 Hz",
		1000: "1 kHz",
		2_000_000_000: "2 GHz",
		2_600_000_000: "2.6 GHz",
		2_660_000_000: "2.66 GHz",
		2_667_000_000: "2.667 GHz",
	}

	for value, expected in values.items():
		assert prettyprinter.print_feature('frequency-hertz', value) == expected


def test_diagonal_inches():
	values = {
		17: "17 in.",
		21: "21 in.",
	}

	for value, expected in values.items():
		assert prettyprinter.print_feature('diagonal-inch', value) == expected


def test_diameter():
	values = {
		10: "10 mm",
		100: "100 mm",
		1000: "1000 mm",
		20: "20 mm",
		200: "200 mm",
		2000: "2000 mm",
	}

	for value, expected in values.items():
		assert prettyprinter.print_feature('diameter-mm', value) == expected


def test_bytes():
	values = {
		10: "10 B",
		100: "100 B",
		1000: "1000 B",
		1024: "1 KiB",
		1024*1024: "1 MiB",
		27*1024*1024: "27 MiB",
		1024*1024*1024: "1 GiB",
		10*1024*1024*1024: "10 GiB",
		11*1024*1024*1024: "11 GiB",
		160*1024*1024*1024: "160 GiB",
		160.1*1024*1024*1024: "160.1 GiB",
		160.12*1024*1024*1024: "160.12 GiB",
		160.123*1024*1024*1024: "160.123 GiB",
		2*1024*1024*1024*1024: "2 TiB",
	}

	for value, expected in values.items():
		assert prettyprinter.print_feature('capacity-byte', value) == expected


def test_hdd_bytes():
	values = {
		10: "10 B",
		100: "100 B",
		1000: "1 kB",
		1024: "1.024 kB",
		1000*1000: "1 MB",
		27*1000*1000: "27 MB",
		1000*1000*1000: "1 GB",
		10*1000*1000*1000: "10 GB",
		11*1000*1000*1000: "11 GB",
		160*1000*1000*1000: "160 GB",
		160.1*1000*1000*1000: "160.1 GB",
		160.12*1000*1000*1000: "160.12 GB",
		160.123*1000*1000*1000: "160.123 GB",
		2*1000*1000*1000*1000: "2 TB",
	}

	for value, expected in values.items():
		assert prettyprinter.print_feature('capacity-decibyte', value) == expected

