import json


def parse_win_chassis_specs(the_dir: str):
    with open(the_dir, "r") as file:
        data = json.load(file)
        object = [
            {
                "features": {
                    "type": "case",
                    "brand": data["Manufacturer"],
                    "sn": data["SerialNumber"],
                }
            }
        ]
        return object


def parse_win_cpu_specs(cpu_dir: str, gpu_dir: str):
    architectures = {
        0: "x86-32",
        1: "mips",
        2: "alpha",
        3: "powerpc",
        6: "ia64",
        9: "x86-64",
    }
    object = []
    with open(cpu_dir, "r") as file:
        data = json.load(file)
        object.append(
            {
                "brand": data["Manufacturer"],
                "model": data["Name"],
                "features": {
                    "type": "cpu",
                    "isa": architectures[data["Architecture"]],
                    "core-n": data["NumberOfCores"],
                    "thread-n": data["ThreadCount"],
                    "frequency-hertz": int(data["MaxClockSpeed"]) * 1000000,
                },
            }
        )
    with open(gpu_dir, "r") as file:
        data = json.load(file)
        for entry in data:
            if "Service" in entry and entry["Service"] == "igfx":
                object[0]["features"]["integrated-graphics-brand"] = entry[
                    "Manufacturer"
                ]
                object[0]["features"]["integrated-graphics-model"] = entry["Name"]
                break
    return json.dumps(object)


def parse_win_ram_specs(the_dir: str):
    with open(the_dir, "r") as file:
        data = json.load(file)
        object = []
        for entry in data:
            object.append(
                {
                    "brand": entry["Manufacturer"],
                    "model": entry["PartNumber"],
                    "features": {
                        "type": "ram",
                        "frequency-hertz": entry["Speed"] * 1000000,
                        "capacity-byte": entry["Capacity"],
                        "ram-type": "",
                        "ram-ecc": "",
                        "ram-timings": "",
                        "sn": entry["SerialNumber"],
                    },
                }
            )
    return json.dumps(object)


def parse_win_motherboard_specs(baseboard_dir: str, pci_dir: str):
    with open(baseboard_dir, "r") as file:
        data = json.load(file)
        object = [
            {
                "brand": data["Manufacturer"],
                "model": data["Product"],
                "features": {
                    "type": "motherboard",
                    "parallel-ports-n": 0,
                    "usb-ports-n": 0,
                    "mini-jack-ports-n": 0,
                    "vga-ports-n": 0,
                    "serial-ports-n": 0,
                    "sata-ports-n": 0,
                    "ide-ports-n": 0,
                    "ps2-ports-n": 0,
                    "ethernet-ports-1000m-n": 0,
                },
            }
        ]
    with open(pci_dir, "r") as file:
        data = json.load(file)
        for entry in data:
            pnp_class = entry["PNPClass"]
            if pnp_class == "USB":
                object[0]["features"]["usb-ports-n"] += 1
                continue
            elif pnp_class == "USB":
                object[0]["features"]["usb-ports-n"] += 1
                continue
            elif pnp_class == "AudioEndpoint":
                object[0]["features"]["mini-jack-ports-n"] += 1
                continue
            elif pnp_class == "DiskDrive":
                object[0]["features"]["sata-ports-n"] += 1
                continue
    return json.dumps(object)
