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

            if "SERIAL_NUMBER" not in device:
                logger.error("Error while parsing device in udevadm - serial number not found")
                logger.error("device:")
                logger.error(device)
                continue

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

            ram_type = device["TYPE"].lower() if "TYPE" in device else None
            size = device["SIZE"] if "SIZE" in device else None
            speed = device["SPEED_MTS"] if "SPEED_MTS" in device else None
            if speed == 666:
                speed = 667
            manufacturer = device["MANUFACTURER"] if "MANUFACTURER" in device else None
            part_number = device["PART_NUMBER"] if "PART_NUMBER" in device else None

            dimm = {
                "type": "ram",
                "working": "yes",
                "ram-type": ram_type,
                "capacity-byte": int(size),
                "brand": manufacturer,
                "model": part_number,
                "sn": sn,
            }
            if speed:
                dimm["frequency-hertz"] = int(speed) * 1000 * 1000
            dimms.append(dimm)
        except KeyError as e:
            _errored = True
            logger.error("Error while parsing device in udevadm")
            logger.error(f"KeyError {e}")
            logger.error("device:")
            logger.error(device)

    if _errored:
        logger.error("file content:")
        for line in file_content.splitlines():
            logger.error(f"\t{line}")
    # MISSING ECC AND TIMINGS

    return dimms
