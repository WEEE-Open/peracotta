#!/usr/bin/python3

"""
Read "lspci -v" and "glxinfo" outputs
"""

import re
from typing import List


def _read_lspci_output(gpu: dict, lspci_file: str, interactive: bool = False):
    lspci_sections = lspci_file.split("\n\n")

    for section in lspci_sections:
        if "VGA compatible controller:" in section:
            # removes "VGA compatible controller:"
            first_line = section.splitlines()[0].split(": ", 1)[1].strip()
            second_line = section.splitlines()[1].strip()
            part_between_square_brackets = None
            try:
                # take the first string between [] from the first line
                part_between_square_brackets = first_line.split("[")[1].split("]")[0]
            except IndexError:
                # there may not be an argument in between []
                pass

            if "Subsystem:" in second_line:
                # The model or model family is often repeated here, but removing it automatically is complicated
                gpu["brand"] = second_line.split("Subsystem: ")[1].split("[", 1)[0].strip()
                gpu["brand"] = gpu["brand"].replace("Integrated Graphics Controller", "").strip()

            # -----------------------------------------------------------------
            # AMD/ATI
            # -----------------------------------------------------------------
            if part_between_square_brackets is not None and ("AMD" in part_between_square_brackets or "ATI" in part_between_square_brackets):
                gpu["brand-manufacturer"] = part_between_square_brackets
                # take second string between []
                gpu["model"] = first_line.split("[")[2].split("]")[0]
                if "controller" in gpu["model"]:
                    gpu["model"] = section.splitlines()[1].split(" ")[-1]

            # -----------------------------------------------------------------
            # Nvidia
            # -----------------------------------------------------------------
            elif "NVIDIA" in first_line.upper():
                gpu["brand-manufacturer"] = "Nvidia"
                gpu["model"] = part_between_square_brackets
                if "brand" in gpu:
                    pieces = gpu["brand"].rsplit(" ", 1)
                    gpu["brand"] = pieces[0]
                    gpu["internal-name"] = pieces[1]

            # -----------------------------------------------------------------
            # Intel
            # -----------------------------------------------------------------
            elif "INTEL" in first_line.upper():
                gpu["brand-manufacturer"] = "Intel"
                if "Integrated Graphics" in first_line:
                    tmp_model = first_line.split("Intel Corporation ")[1].split(" Integrated Graphics")[0]
                    # if there are no numbers, e.g. "Core Processor", tmp_model is not a model number
                    if not re.search("\\d+", tmp_model):
                        tmp_model = ""
                elif "HD Graphics" in first_line:
                    tmp_model = first_line.split("Intel Corporation ")[1].split("(", 1)[0].strip()
                elif "[" in first_line and "]" in first_line:
                    tmp_model = first_line.split("[")[1].split("]")[0]
                else:
                    tmp_model = ""

                if tmp_model != "":
                    gpu["model"] = tmp_model

            # -----------------------------------------------------------------
            # VIA
            # -----------------------------------------------------------------
            elif first_line.startswith("VIA"):
                gpu["brand-manufacturer"] = "VIA"
                gpu["model"] = part_between_square_brackets

                tmp_model = first_line.split("[")[0]
                i = 0
                for i, char in enumerate("VIA Technologies, Inc. "):
                    if tmp_model[i] != char:
                        break
                gpu["internal-name"] = tmp_model[i:].strip()

            # -----------------------------------------------------------------
            # SiS
            # -----------------------------------------------------------------
            elif part_between_square_brackets == "SiS":
                # May be written somewhere else on other models, but we have so few SiS cards that it's difficult to
                # find more examples. Also, they haven't made any video card in the last 15 years or so.
                gpu["brand-manufacturer"] = part_between_square_brackets
                if "brand" in gpu and gpu["brand"].lower() == "silicon integrated systems":
                    gpu["brand"] = "SiS"
                gpu["model"] = first_line.split("]", 1)[1]
                # These may be useful for non-integrated cards, however the example ones are all integrated
                if " PCIE" in gpu["model"]:
                    gpu["model"] = gpu["model"].split(" PCIE", 1)[0].strip()
                elif " PCI/AGP" in gpu["model"]:
                    gpu["model"] = gpu["model"].split(" PCI/AGP", 1)[0].strip()
                if gpu["model"] in gpu["brand"]:
                    gpu["brand"] = gpu["brand"].split(gpu["model"], 1)[0].strip()
            else:
                gpu["brand-manufacturer"] = None
                if interactive:
                    print(
                        "I couldn't find the Video Card brand. The model was set to 'None' and is to be edited "
                        "logging into the TARALLO afterwards. The information you're looking for should be in the "
                        f"following 2 lines:\n{first_line}\n{second_line}\n"
                    )

            if gpu.get("model") and gpu.get("brand"):
                # Try to remove duplicate information
                gpu["brand"] = gpu["brand"].replace(gpu["model"], "").strip()
            else:
                if interactive:
                    print(
                        "I couldn't find the Integrated Graphics model. The model was set to 'None' and is to be "
                        "edited logging into the TARALLO afterwards. The information you're looking for should be in "
                        f"the following 2 lines:\n{first_line}\n{second_line}\n"
                    )
            break

    if gpu.get("internal-name"):
        # Same
        gpu["brand"] = gpu["brand"].replace(gpu["internal-name"], "").strip()

    if gpu.get("brand") == "":
        del gpu["brand"]

    if gpu.get("brand-manufacturer") and gpu.get("brand"):
        if gpu["brand-manufacturer"].lower() == gpu["brand"].lower():
            del gpu["brand-manufacturer"]

    if interactive:
        if "brand" not in gpu and "brand-manufacturer" not in gpu:
            print(
                "I couldn't find the Video Card brand. The model was set to 'None' and is to be edited logging "
                "into the TARALLO afterwards. The information you're looking for should be in the following 2 lines:"
            )
        if "capacity-byte" not in gpu:
            print(
                "A dedicated video memory couldn't be found. A generic video memory capacity was found instead, which "
                "could be near the actual value. Please humans, fix this error by hand."
            )


def _read_glxinfo_output(gpu: dict, glxinfo_file: str):
    for line in glxinfo_file.splitlines():
        # this line comes before the "Dedicated video memory" line
        # this basically saves a default value if the dedicated memory line cannot be found
        if "Video memory" in line:
            try:
                tmp_vid_mem = int(line.split(" ")[6].split(" ")[0][:-2])
                tmp_vid_mem_multiplier = line[-2:]
            except ValueError:
                continue

            _parse_capacity(gpu, tmp_vid_mem, tmp_vid_mem_multiplier)
            break

        if "Dedicated video memory" in line:
            try:
                tmp_vram = int(line.split(" ")[7].split(" ")[0])
                tmp_vram_multiplier = line[-2:]
            except ValueError:
                continue

            _parse_capacity(gpu, tmp_vram, tmp_vram_multiplier)
            break

    if not gpu.get("capacity-byte"):
        if "notes" in gpu:
            gpu["notes"] += "\n"
        else:
            gpu["notes"] = ""
        gpu["notes"] += "Could not find dedicated video memory, check glxinfo output"


def _parse_capacity(gpu, tmp_vram, tmp_vram_multiplier):
    capacity = _convert_video_memory_size(tmp_vram, tmp_vram_multiplier)
    # Round to the next power of 2
    # this may be different from human readable capacity...
    rounded = 2 ** (capacity - 1).bit_length()
    one_and_half = int(rounded / 2 * 1.5)
    # Accounts for 3 GB VRAM cards and similar
    # Yes they do exist, try to remove this part and watch tests fail (and the card was manually verified to be 3 GB)
    if one_and_half >= capacity:
        gpu["capacity-byte"] = one_and_half
    else:
        gpu["capacity-byte"] = rounded


def _convert_video_memory_size(capacity, units_of_measure):
    if units_of_measure == "GB":
        capacity *= 1024 * 1024 * 1024
    elif units_of_measure == "MB":
        capacity *= 1024 * 1024
    elif units_of_measure.upper() == "KB":
        capacity *= 1024
    else:
        capacity = -1

    return capacity


def parse_lspci_and_glxinfo(has_dedicated: bool, lspci_file: str, glxinfo_file: str, interactive: bool = False) -> List[dict]:
    gpu = {
        "type": "graphics-card",
        "working": "yes",
    }
    if has_dedicated:
        _read_lspci_output(gpu, lspci_file, interactive)
        _read_glxinfo_output(gpu, glxinfo_file)
    else:
        # integrated in mobo or cpu
        _read_lspci_output(gpu, lspci_file, interactive)
        # don't parse glxinfo because the VRAM is part of the RAM and varies
        if "capacity-byte" in gpu:
            del gpu["capacity-byte"]

    return [gpu]


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Parse lspci/glxinfo output")
    parser.add_argument("lspci", type=str, nargs=1, help="path to lspci output")
    parser.add_argument("glxinfo", type=str, nargs=1, help="path to glxinfo output")
    parser.add_argument(
        "-d",
        "--dedicated",
        action="store_true",
        default=False,
        help="computer has dedicated GPU",
    )
    args = parser.parse_args()

    try:
        with open(args.lspci[0], "r") as f:
            input_lspci = f.read()
        with open(args.glxinfo[0], "r") as f:
            input_glxinfo = f.read()

        print(
            json.dumps(
                parse_lspci_and_glxinfo(args.dedicated, input_lspci, input_glxinfo),
                indent=2,
            )
        )
    except FileNotFoundError as e:
        print(str(e))
        exit(1)
