#!/usr/bin/python3

# initial_chars_to_ignore is the length of the feature whose name the line begins with
# e.g. "Fundamental Memory Type" begins with 23 characters that are not all spaces, then n spaces to ignore,
# and finally there's the value needed, e.g. "DDR3 SDRAM"
from typing import List


def _ignore_spaces(line: str, initial_chars_to_ignore: int):
    relevant_part = line[initial_chars_to_ignore:]
    return relevant_part.strip()


def parse_decode_dimms(dimms: str, interactive: bool = False) -> List[dict]:
    # check based on output of decode-dimms v6250
    if "Number of SDRAM DIMMs detected and decoded: 0" in dimms or "Number of SDRAM DIMMs detected and decoded: " not in dimms:
        if interactive:
            print("decode-dimms was not able to find any RAM details")
        return []

    # split strings in 1 str array for each DIMM
    dimm_sections = dimms.split("Decoding EEPROM")
    # remove useless first part
    del dimm_sections[0]

    # create list of as many dimms as there are dimm_sections
    dimms = [
        {
            "type": "ram",
            "working": "yes",
        }
        for _ in range(len(dimm_sections))
    ]

    for i, dimm in enumerate(dimm_sections):
        manufacturer_data_type = None
        for line in dimm.splitlines():
            if line.startswith("Fundamental Memory type"):
                dimms[i]["ram-type"] = line.split(" ")[-2].lower()
                if dimms[i]["ram-type"] == "unknown":
                    del dimms[i]["ram-type"]

            if line.startswith("Maximum module speed"):
                freq = line.split(" ")[-3:-1]
                dimms[i]["frequency-hertz"] = int(freq[0])
                if "KHz" in freq[1] or "kHz" in freq[1]:
                    dimms[i]["frequency-hertz"] *= 1000
                elif "MHz" in freq[1]:
                    dimms[i]["frequency-hertz"] *= 1000 * 1000
                elif "GHz" in freq[1]:
                    dimms[i]["frequency-hertz"] *= 1000 * 1000 * 1000
                # The official thing is 667 MHz even if they run at 666 MHz
                if dimms[i]["frequency-hertz"] == 666000000:
                    dimms[i]["frequency-hertz"] = 667000000

            if line.startswith("Size"):
                cap = line.split(" ")[-2:]
                dimms[i]["capacity-byte"] = int(cap[0])
                if "KB" in cap[1] or "kB" in cap[1]:
                    dimms[i]["capacity-byte"] *= 1024
                elif "MB" in cap[1]:
                    dimms[i]["capacity-byte"] *= 1024 * 1024
                elif "GB" in cap[1]:
                    dimms[i]["capacity-byte"] *= 1024 * 1024 * 1024

            # alternatives to "Manufacturer" are "DRAM Manufacturer" and "Module Manufacturer"
            if "---=== Manufacturer Data ===---" in line:
                manufacturer_data_type = "DRAM Manufacturer"

            if "---=== Manufacturing Information ===---" in line:
                manufacturer_data_type = "Manufacturer"

            if manufacturer_data_type and line.startswith(manufacturer_data_type):
                dimms[i]["brand"] = _ignore_spaces(line, len(manufacturer_data_type))

            # This seems to always be the model (or at least never be the serial number)
            if line.startswith("Part Number"):
                model = _ignore_spaces(line, len("Part Number"))
                if model.lower() != "undefined":
                    dimms[i]["model"] = model

            # part number can be overwritten by serial number if present
            if line.startswith("Assembly Serial Number"):
                dimms[i]["sn"] = _ignore_spaces(line, len("Assembly Serial Number"))
                if dimms[i]["sn"].startswith("0x"):
                    try:
                        dimms[i]["sn"] = str(int(dimms[i]["sn"][2:], base=16))
                    except ValueError:
                        # Ooops, this isn't an hex number after all...
                        pass

            if line.startswith("Module Configuration Type"):
                if "Data Parity" in line or "Data ECC" in line or "Address/Command Parity" in line:
                    dimms[i]["ram-ecc"] = "yes"
                else:
                    dimms[i]["ram-ecc"] = "no"

            # Two (or more) spaces after because there are lines like "tCL-tRCD-tRP-tRAS as ..."
            if line.startswith("tCL-tRCD-tRP-tRAS  "):
                dimms[i]["ram-timings"] = _ignore_spaces(line, len("tCL-tRCD-tRP-tRAS"))

        if "ram-ecc" not in dimms[i] and len(dimms[i]) > 2:
            dimms[i]["ram-ecc"] = "no"

    return dimms


if __name__ == "__main__":
    import json
    import sys

    try:
        with open(sys.argv[1], "r") as f:
            input_file = f.read()
        print(json.dumps(parse_decode_dimms(input_file), indent=2))
    except BaseException as e:
        print(str(e))
        exit(1)
