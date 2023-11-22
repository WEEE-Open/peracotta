def print_feature(feature, value, feature_type=None):
    unit = _name_to_unit(feature)
    if unit is None:
        if feature_type == "i":
            return int(value)
        elif feature_type == "d":
            return float(value)
        else:
            return str(value)
    else:
        return _print_value(unit, value)


def name_to_unit(name):
    return name.split("-")[-1]


def printable_to_value(unit, input_value):
    if not isinstance(input_value, str):
        return input_value
    string = input_value.strip()
    if len(string) <= 0:
        raise ValueError
    if unit == "n":
        return int(input_value)

    i = 0
    pure = False
    for i in range(0, len(input_value)):
        if not (input_value[i].isdigit() or (input_value[i] in (".", ","))):
            break
    else:
        pure = True

    if pure:
        number = float(input_value)
    else:
        if i == 0:
            raise ValueError
        number = float(input_value[0:i])

    exp = 0
    if unit == "mm":
        exp = 0
    elif pure:
        exp = 0
    else:
        for char in input_value[i:]:
            char = char.lower()
            if char.isalpha():
                exp = _prefix_to_exponent(char)
                break
    if unit == "byte":
        base = 1024
    else:
        base = 1000

    return number * (pow(base, exp))


def _prefix_to_exponent(char):
    if char == "k":
        return 1
    if char == "m":
        return 2
    if char == "g":
        return 3
    if char == "t":
        return 4
    if char == "p":
        return 5
    if char == "e":
        return 6
    return 0


def _name_to_unit(name):
    pieces = name.split("-")
    units = {
        "byte": "byte",
        "hertz": "Hz",
        "decibyte": "B",
        "ampere": "A",
        "volt": "V",
        "watt": "W",
        "rpm": "rpm",
        "mm": "mm",
        "inch": "in.",
        "gram": "g",
    }
    if pieces[-1] in units:
        return units[pieces[-1]]
    else:
        return None


def _print_value(unit, value):
    if unit == "n":
        return str(value)
    elif unit == "rpm" or unit == "mm" or unit == "in.":
        return f"{_format_value(value)} {unit}"
    elif unit == "byte":
        return _append_unit(value, "B", 1024)
    else:
        return _append_unit(value, unit, 1000)


def _append_unit(value, unit, base_unit=1000):
    prefix = 0
    while value >= base_unit and prefix <= 6:
        value /= base_unit
        prefix += 1
    i = ""
    if prefix > 0 and base_unit == 1024:
        i = "i"
    return f"{_format_value(value)} {_prefix_to_printable(prefix, base_unit == 1024)}{i}{unit}"


def _format_value(value: float):
    return f"{value:g}"


def _prefix_to_printable(places, big_k=False):
    prefixes = {
        0: "",
        1: "K" if big_k else "k",
        2: "M",
        3: "G",
        4: "T",
        5: "P",
        6: "E",
        # -1: 'm',
        # -2: 'µ',
        # -3: 'n',
    }
    return prefixes[places]
