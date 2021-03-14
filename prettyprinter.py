def print_feature(feature, value):
	unit = _name_to_unit(feature)
	if unit is None:
		return str(value)
	else:
		return _print_value(unit, value)


def _name_to_unit(name):
	pieces = name.split('-')
	units = {
		'byte': 'byte',
		'hertz': 'Hz',
		'decibyte': 'B',
		'ampere': 'A',
		'volt': 'V',
		'watt': 'W',
		'rpm': 'rpm',
		'mm': 'mm',
		'inch': 'in.',
		'gram': 'g',
	}
	if pieces[-1] in units:
		return units[pieces[-1]]
	else:
		return None


def _print_value(unit, value):
	if unit == 'n':
		return str(value)
	elif unit == 'rpm' or unit == 'mm' or unit == 'in.':
		return f"{_format_value(value)} {unit}"
	elif unit == 'byte':
		return _append_unit(value, 'B', 1024)
	else:
		return _append_unit(value, unit, 1000)


def _append_unit(value, unit, base_unit=1000):
	prefix = 0
	while value >= base_unit and prefix <= 6:
		value /= base_unit
		prefix += 1
	i = ''
	if prefix > 0 and base_unit == 1024:
		i = 'i'
	return f"{_format_value(value)} {_prefix_to_printable(prefix, base_unit == 1024)}{i}{unit}"


def _format_value(value: float):
	return f"{value:g}"


def _prefix_to_printable(places, big_k=False):
	prefixes = {
		0: '',
		1: 'K' if big_k else 'k',
		2: 'M',
		3: 'G',
		4: 'T',
		5: 'P',
		6: 'E',
		# -1: 'm',
		# -2: 'µ',
		# -3: 'n',
	}
	return prefixes[places]
