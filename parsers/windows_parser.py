import json


def parse_win_chassis_specs(the_dir: str):
    with open(f"{the_dir}/chassis.win", "r") as file:
        data = json.load(file)
        object = [
            {
                "features": {
                    "brand": data["Manufacturer"],
                    "sn": data["SerialNumber"],
                },
                "type": "case",
            }
        ]
        return object


def parse_win_cpu_specs(the_dir: str):
    architectures = {
        0: "x86-32",
        1: "mips",
        2: "alpha",
        3: "powerpc",
        6: "ia64",
        9: "x86-64",
    }
    object = []
    with open(f"{the_dir}/lscpu.win", "r") as file:
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
                "type": "cpu",
            }
        )
    with open(f"{the_dir}/graphics.win", "r") as file:
        data = json.load(file)
        for entry in data:
            if "Service" in entry and entry["Service"] == "igfx":
                object[0]["features"]["integrated-graphics-brand"] = entry["Manufacturer"]
                object[0]["features"]["integrated-graphics-model"] = entry["Name"]
                break
    return object


def parse_win_ram_specs(the_dir: str):
    with open(f"{the_dir}/dimms.win", "r") as file:
        data = json.load(file)
        object = []
        for entry in data:
            object.append(
                {
                    "brand": entry["Manufacturer"],
                    "model": entry["PartNumber"],
                    "features": {
                        "frequency-hertz": entry["Speed"] * 1000000,
                        "capacity-byte": entry["Capacity"],
                        "ram-type": "",
                        "ram-ecc": "",
                        "ram-timings": "",
                        "sn": entry["SerialNumber"],
                    },
                    "type": "ram",
                }
            )
    return object


def parse_win_motherboard_specs(the_dir: str):
    with open(f"{the_dir}/baseboard.win", "r") as file:
        data = json.load(file)
        object = [
            {
                "brand": data["Manufacturer"],
                "model": data["Product"],
                "features": {
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
                "type": "motherboard",
            }
        ]
    with open(f"{the_dir}/lspci.win", "r") as file:
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
    return object
