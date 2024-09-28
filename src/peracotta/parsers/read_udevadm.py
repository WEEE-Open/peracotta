from typing import List

from peracotta.peralog import logger


def parse_udevadm(file_content: str) -> List[dict]:
    devices = {}
    for line in file_content.splitlines():

        if not line.startswith("E:"):
            logger.error(f"Expected 'E:' at the beginning of line: {line}")
            logger.error(f"\n{file_content}")
            raise ValueError("Error while parsing udevadm output")

        key, value = line[3:].split("=")

        if not key[:14].startswith("MEMORY_DEVICE_"):
            logger.error(f"Expected 'MEMORY_DEVICE' at the beginning of key: {key}")
            logger.error(f"\n{file_content}")
            raise ValueError("Error while parsing udevadm output")

        device_id = key[14:].split("_")[0]  # could have taken a single char but this is more reliable

        if device_id not in devices:
            devices[device_id] = {}
        devices[device_id][key[15 + len(device_id) :]] = value.strip()

    dimms = []
    for device_id, device in devices.items():
        if device["SPEED_MTS"] == 666:
            device["SPEED_MTS"] = 667

        if device["SERIAL_NUMBER"][0:2] == "0x":
            device["SERIAL_NUMBER"] = str(int(device["SERIAL_NUMBER"][2:], base=16))
        if any(c in "abcdefABCDEF" for c in device["SERIAL_NUMBER"]):
            device["SERIAL_NUMBER"] = str(int(device["SERIAL_NUMBER"], base=16))

        dimm = {
            "type": "ram",
            "working": "yes",
            "ram-type": device["TYPE"].upper(),
            "frequency-hertz": int(device["SPEED_MTS"]) * 1000 * 1000,
            "capacity-byte": int(device["SIZE"]),
            "brand": device["MANUFACTURER"],
            "model": device["PART_NUMBER"],
            "sn": device["SERIAL_NUMBER"],
        }
        dimms.append(dimm)

    # MISSING ECC AND TIMINGS

    return dimms
