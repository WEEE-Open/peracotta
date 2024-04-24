#!/usr/bin/env python3
from typing import List, Optional

connectors_map = {
    "PS/2": "ps2-ports-n",
    "Access Bus (USB)": "usb-ports-n",
    "DB-25 male": "parallel-ports-n",
    "DB-25 female": "parallel-ports-n",
    "DB-9 male": "serial-ports-n",
    "DB-15 female": "vga-ports-n",
    "Mini Jack (headphones)": "mini-jack-ports-n",
    "RJ-45": "ethernet-ports-n",  # not a real feature in T.A.R.A.L.L.O., since it's not yet known if it's 100 or 1000
    "Mini DisplayPort": "mini-displayport-ports-n",
    "Thunderbolt": "thunderbolt-ports-n",
    "HDMI": "hdmi-ports-n",
    "SATA0": "sata-ports-n",
    "SATA1": "sata-ports-n",
    "SATA2": "sata-ports-n",
    "SATA3": "sata-ports-n",
    "SATA4": "sata-ports-n",
    "SATA5": "sata-ports-n",
    "SATA6": "sata-ports-n",
    "SATA7": "sata-ports-n",
    "USB0": "usb-ports-n",
    "USB1": "usb-ports-n",
    "USB2": "usb-ports-n",
    "USB3": "usb-ports-n",
    "USB4": "usb-ports-n",
    "USB5": "usb-ports-n",
    "USB6": "usb-ports-n",
    "USB7": "usb-ports-n",
    "USB8": "usb-ports-n",
    "LINE_IN": "mini-jack-ports-n",
    "IEEE 1394": "firewire-ports-n",
    "RJ-11": "rj11-ports-n",
    "On Board Sound Input From CD-ROM": None,
    "On Board Floppy": None,
    "CHASSIS REAR FAN": None,
    "CHASSIS FAN": None,
    "CPU FAN": None,
    "FNT USB": None,
    "FP AUD": None,
    "ATX_PWR": None,
    "9 Pin Dual Inline (pin 10 cut)": None,  # Internal USB header?
    "Microphone": None,  # Internal microphone, not a connector
    "Speaker": None,
    "SPEAKER (SPKR)": None,  # Internal speaker (header)
    "FP_AUDIO": None,
    "PASSWORD CLEAR (PSWD)": None,
    "HOOD LOCK (HLCK)": None,
    "HOOD SENSE (HSENSE)": None,
    "TPM SECURITY (SEC)": None,
}
connectors_map_tuples = {
    ("On Board IDE", None, "*IDE*", None): "ide-ports-n",
    ("On Board IDE", None, None, "* IDE"): "ide-ports-n",
    ("On Board IDE", None, "PRIMARY*", None): "ide-ports-n",
    ("On Board IDE", None, "SECONDARY*", None): "ide-ports-n",
    (None, None, "*ESATA*", None): "esata-ports-n",
    ("On Board IDE", None, "SATA*", None): "sata-ports-n",
    (
        "On Board IDE",
        None,
        "*SATA*",
        None,
    ): "sata-ports-n",  # Don't add *SATA, it matches ESATA...
    (None, None, None, "REAR LINE IN"): "mini-jack-ports-n",
    (None, None, None, "REAR HEADPHONE/LINEOUT"): "mini-jack-ports-n",
    (None, None, "*FAN", None): None,
    (None, None, "CHA_FAN*", None): None,
    (None, None, "FRNT AUD*", None): None,  # Front audio is not part of the motherboard
    ("SAS/SATA Plug Receptacle", None, "SATA*", None): "sata-ports-n",
    ("SAS/SATA Plug Receptacle", None, "*EIDE", None): "ide-ports-n",
    ("SAS/SATA Plug Receptacle", None, "SAS*", None): "sas-sata-ports-n",
}
extra_connectors = {
    "MagSafe DC Power": {"power-connector": "proprietary"},
}


def parse_motherboard(baseboard_file: str, connectors_file: str, net_file: str, interactive: bool = False) -> List[dict]:
    baseboard = _get_baseboard(baseboard_file)
    baseboard = _get_connectors(connectors_file, baseboard, interactive)
    baseboards = _get_net(net_file, baseboard, interactive)
    return baseboards


def _get_baseboard(baseboard: str) -> dict:
    mobo = {
        "type": "motherboard",
        "working": "yes",
    }

    for line in baseboard.splitlines():
        if "Manufacturer:" in line:
            mobo["brand"] = line.split("Manufacturer:")[1].strip()

        elif "Product Name:" in line:
            mobo["model"] = line.split("Product Name:")[1].strip()

        elif "Serial Number:" in line:
            mobo["sn"] = line.split("Serial Number:")[1].strip().strip(".")

    # Get MSI internal codename
    if mobo.get("brand", "").upper().startswith("MICRO-STAR INTERNATIONAL"):
        model = mobo.get("model", "")
        model_parts = model.split("(")
        if len(model_parts) == 2:
            mobo["model"] = model_parts[0].strip()
            mobo["internal-name"] = model_parts[1].rstrip(")").strip()

    return mobo


def _get_connectors(connectors_file: str, baseboard: dict, interactive: bool = False) -> dict:
    possible_connectors = set(connectors_map.values()) | set(connectors_map_tuples.values())
    possible_connectors.remove(None)
    connectors = dict(zip(possible_connectors, [0] * len(connectors_map)))

    # TODO: this part (is it needed?)
    # port_types = []
    # devices = output.split("On Board Device")
    # for device in devices:
    # 	type = device.split("Description:")
    # 	if len(type) > 1:
    # 		port_types.append(type[1].replace("\n", "").replace(" ", ""))

    warnings = []
    for section in connectors_file.split("\n\n"):
        if not section.startswith("Handle "):
            continue
        internal = get_dmidecoded_value(section, "Internal Connector Type:")
        external = get_dmidecoded_value(section, "External Connector Type:")
        internal_des = get_dmidecoded_value(section, "Internal Reference Designator:")
        external_des = get_dmidecoded_value(section, "External Reference Designator:")
        if external in ("None", "Other", "Not Specified"):
            if internal in ("None", "Other", "Not Specified"):
                if external_des in ("None", "Other", "Not Specified"):
                    connector = internal_des
                else:
                    connector = external_des
            else:
                connector = internal
        else:
            connector = external

        if connector in connectors_map:
            if connectors_map[connector] is not None:
                connectors[connectors_map[connector]] += 1
        elif connector in extra_connectors:
            # Dark magic: https://stackoverflow.com/a/26853961
            connectors = {**connectors, **(extra_connectors[connector])}
        else:
            found = find_connector_from_tuple(connectors, external, external_des, internal, internal_des)
            if not found:
                warning = f"Unknown connector: {internal} / {external} ({internal_des} / {external_des})"
                if interactive:
                    print(warning)
                warnings.append(warning)

    connectors_clean = {}
    # Keys to avoid changing dict size at runtime (raises an exception)
    for connector in connectors:
        if isinstance(connectors[connector], int):
            if connectors[connector] > 0:
                connectors_clean[connector] = connectors[connector]
        else:
            connectors_clean[connector] = connectors[connector]

    if len(warnings) > 0:
        warnings = "\n".join(warnings)
        # Dark magic: https://stackoverflow.com/a/26853961
        return {**baseboard, **connectors_clean, **{"notes": warnings}}
    else:
        # Somewhat less dark magic
        return {**baseboard, **connectors_clean}


def _get_net(net: str, baseboard: dict, interactive: bool = False) -> List[dict]:
    mergeit = {
        "ethernet-ports-100m-n": 0,
        "ethernet-ports-1000m-n": 0,
        "mac": [],
    }
    other_devices = []

    for line in net.split("\n"):
        if "u" in line:
            # USB adapters, ignore them
            continue
        line = line.split(" ", 3)
        if line[0].startswith("en"):
            if interactive and len(line) <= 2:
                print(f"Warning: cannot detect speed for Ethernet port {line[0]}, is it unconnected?")
            elif line[2] == "1000":
                mergeit["ethernet-ports-1000m-n"] += 1
            elif line[2] == "100":
                mergeit["ethernet-ports-100m-n"] += 1
            elif interactive:
                print(f"Warning: unknown speed for Ethernet port {line[0]}: {line[2]}")
            mergeit["mac"].append(line[1])
        if line[0].startswith("wl"):
            other_devices.append({"type": "wifi-card", "mac": line[1], "notes": f"Device name {line[0]}"})

    mergeit["mac"] = ", ".join(mergeit["mac"])

    if "ethernet-ports-n" in baseboard:
        found_ports = mergeit["ethernet-ports-100m-n"] + mergeit["ethernet-ports-1000m-n"]
        baseboard["ethernet-ports-n"] -= found_ports
        if baseboard["ethernet-ports-n"] > 0:
            if baseboard["ethernet-ports-n"] > 1:
                message = f"\nBIOS reported {baseboard['ethernet-ports-n']} more ethernet ports that were not found by the kernel"
            else:
                message = f"\nBIOS reported {baseboard['ethernet-ports-n']} more ethernet port that was not found by the kernel"
            if "notes" in baseboard:
                baseboard["notes"] += message
                baseboard["notes"] = baseboard["notes"].strip()
            else:
                baseboard["notes"] = message.strip()
        del baseboard["ethernet-ports-n"]

    if mergeit["ethernet-ports-100m-n"] <= 0:
        del mergeit["ethernet-ports-100m-n"]
    if mergeit["ethernet-ports-1000m-n"] <= 0:
        del mergeit["ethernet-ports-1000m-n"]
    if len(mergeit["mac"]) <= 0:
        del mergeit["mac"]
    baseboard = {**baseboard, **mergeit}

    # It even says the type is the exact same one it expects, however it's an error
    # noinspection PyTypeChecker
    return [baseboard] + other_devices


def find_connector_from_tuple(connectors, external, external_des, internal, internal_des):
    equal = False
    for tup in connectors_map_tuples:
        zipped = list(zip(tup, (internal, external, internal_des, external_des)))
        equal = True
        for mask, garbage_from_manufacturer in zipped:
            if mask is None:
                continue
            if mask.startswith("*") and mask.endswith("*"):
                if mask[1:-1] not in garbage_from_manufacturer:
                    equal = False
                    break
            elif mask.endswith("*"):
                if not garbage_from_manufacturer.startswith(mask[:-1]):
                    equal = False
                    break
            elif mask.startswith("*"):
                if not garbage_from_manufacturer.endswith(mask[1:]):
                    equal = False
                    break
            elif mask != garbage_from_manufacturer:
                equal = False
                break
        if equal:
            if connectors_map_tuples[tup] is not None:
                connectors[connectors_map_tuples[tup]] += 1
            return equal
    return equal


def get_dmidecoded_value(section: str, key: str) -> str:
    return section.split(key, 1)[1].split("\n", 1)[0].strip()


def parse_psu(chassis: Optional[dict]):
    if chassis.get("motherboard-form-factor") == "proprietary-laptop":
        return [{"type": "external-psu", "check": "missing-data", "working": "yes"}]
    else:
        return [{"type": "psu", "check": "missing-data", "working": "yes"}]


def parse_case(chassis_file: str, mobo: Optional[dict] = None) -> List[dict]:
    chassis = {"type": "case"}

    for line in chassis_file.splitlines():
        if "Manufacturer" in line:
            manufacturer = line.split("Manufacturer:")[1].strip()
            if len(manufacturer) > 0:
                chassis["brand"] = manufacturer

        # This is Desktop, Laptop, etc...
        elif "Type: " in line:
            ff = line.split("Type: ")[1].strip()
            if ff == "Laptop" or ff == "Notebook":  # Both exist in the wild and in tests, difference unknown
                chassis["motherboard-form-factor"] = "proprietary-laptop"
                if mobo and "motherboard-form-factor" not in mobo:
                    mobo["motherboard-form-factor"] = "proprietary-laptop"

        elif "Serial Number" in line:
            sn = line.split("Serial Number:")[1].strip().strip(".")
            if len(sn.strip("0")) <= 0:
                sn = ""
            if len(sn) > 0:
                chassis["sn"] = sn

    for key, value in chassis.items():
        if value == "Unknown":
            # Remove pointless values
            del chassis[key]

    return [chassis]


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Parse dmidecode output")
    parser.add_argument("-b", "--baseboard", type=str, help="Path to baseboard.txt")
    parser.add_argument("-c", "--chassis", type=str, help="Path to chassis.txt")
    parser.add_argument("-p", "--ports", type=str, help="Path to connector.txt (ports)")
    parser.add_argument("-n", "--net", type=str, help="Path to net.txt")
    args = parser.parse_args()

    if args.ports is not None and args.baseboard is None:
        print("Provide a baseboard.txt file to detect connectors")
        exit(2)
    if args.net is not None and args.baseboard is None:
        print("Provide a baseboard.txt file to detect network cards")
        exit(2)
    if args.baseboard is not None and args.ports is None:
        print("Provide a connector.txt file to parse motherboard")
        exit(2)
    if args.baseboard is not None and args.net is None:
        print("Provide a net.txt file to parse motherboard")
        exit(2)

    try:
        if args.baseboard is not None:
            with open(args.baseboard, "r") as f:
                input_baseboard = f.read()
            with open(args.ports, "r") as f:
                input_ports = f.read()
            with open(args.ports, "r") as f:
                input_net = f.read()
            bb = parse_motherboard(input_baseboard, input_ports, input_net, True)
            print(json.dumps(bb, indent=2))
        if args.chassis is not None:
            with open(args.chassis, "r") as f:
                input_chassis = f.read()
            try:
                # This pointless check triggers NameError if bb is not defined
                # noinspection PyUnboundLocalVariable
                if bb is None:
                    pass
            except NameError:
                bb = None

            # bb is bery well defined, Pycharm doesn't believe it though
            # noinspection PyUnboundLocalVariable
            print(json.dumps(parse_case(input_chassis, bb), indent=2))

    except FileNotFoundError as e:
        print(str(e))
        exit(1)
