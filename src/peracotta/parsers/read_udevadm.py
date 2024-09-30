from typing import List

from peracotta.peralog import logger


def parse_udevadm(file_content: str) -> List[dict]:
    devices = {}
    _errored = False

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
        try:
            if device["SPEED_MTS"] == 666:
                device["SPEED_MTS"] = 667

            try:
                if device["SERIAL_NUMBER"][0:2] == "0x":
                    sn = str(int(device["SERIAL_NUMBER"][2:], base=16))
                if any(c in "abcdefABCDEF" for c in device["SERIAL_NUMBER"]):
                    sn = str(int(device["SERIAL_NUMBER"], base=16))
                else:
                    sn = device["SERIAL_NUMBER"]
            except ValueError:
                logger.error(f"Error while parsing serial number: {device['SERIAL_NUMBER']}")
                logger.error(f"{file_content = }")
                continue

            if sn:
                dimm = {
                    "type": "ram",
                    "working": "yes",
                    "ram-type": device["TYPE"].upper(),
                    "frequency-hertz": int(device["SPEED_MTS"]) * 1000 * 1000,
                    "capacity-byte": int(device["SIZE"]),
                    "brand": device["MANUFACTURER"],
                    "model": device["PART_NUMBER"],
                    "sn": sn,
                }
                dimms.append(dimm)
        except KeyError as e:
            logger.error(f"{e}")
            logger.error(f"Error while parsing device in udevadm: {device}")
            logger.error("file content:")
            for line in file_content.splitlines():
                logger.error(f"\t{line}")
            continue
    # MISSING ECC AND TIMINGS

    return dimms
