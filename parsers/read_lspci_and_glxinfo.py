#!/usr/bin/python3

"""
Read "lspci -v" and "glxinfo" outputs
"""

import re
from dataclasses import dataclass

from InputFileNotFoundError import InputFileNotFoundError


@dataclass
class VideoCard:
    type = "graphics-card"
    manufacturer_brand = ""
    reseller_brand = ""
    internal_name = ""
    model = ""
    capacity = -1  # bytes
    warning = ""


def parse_lspci_output(gpu: VideoCard, lspci_path: str, interactive: bool = False):
    try:
        with open(lspci_path, "r") as f:
            lspci_output = f.read()
    except FileNotFoundError:
        raise InputFileNotFoundError(lspci_path)

    lspci_sections = lspci_output.split("\n\n")

    for section in lspci_sections:
        if "VGA compatible controller" in section:
            first_line = section.splitlines()[0].split(": ", 1)[
                1
            ]  # removes "VGA compatible controller:"
            second_line = section.splitlines()[1]
            part_between_square_brackets = None
            try:
                # take the first string between [] from the first line
                part_between_square_brackets = first_line.split("[")[1].split("]")[0]
            except IndexError:
                # there may not be an argument in between []
                pass

            if "Subsystem:" in second_line:
                # The model or model family is often repeated here, but removing it automatically is complicated
                gpu.reseller_brand = (
                    second_line.split("Subsystem: ")[1].split("[", 1)[0].strip()
                )
                gpu.reseller_brand = gpu.reseller_brand.replace(
                    "Integrated Graphics Controller", ""
                )

            # -----------------------------------------------------------------
            # AMD/ATI
            # -----------------------------------------------------------------
            if part_between_square_brackets is not None and (
                "AMD" in part_between_square_brackets
                or "ATI" in part_between_square_brackets
            ):
                gpu.manufacturer_brand = part_between_square_brackets
                # take second string between []
                gpu.model = first_line.split("[")[2].split("]")[0]
                if "controller" in gpu.model:
                    gpu.model = section.splitlines()[1].split(" ")[-1]

            # -----------------------------------------------------------------
            # Nvidia
            # -----------------------------------------------------------------
            elif "NVIDIA" in first_line.upper():
                gpu.manufacturer_brand = "Nvidia"
                gpu.model = part_between_square_brackets
                if gpu.reseller_brand != "":
                    pieces = gpu.reseller_brand.rsplit(" ", 1)
                    gpu.reseller_brand = pieces[0]
                    gpu.internal_name = pieces[1]

            # -----------------------------------------------------------------
            # Intel
            # -----------------------------------------------------------------
            elif "INTEL" in first_line.upper():
                gpu.manufacturer_brand = "Intel"
                if "Integrated Graphics" in first_line:
                    tmp_model = first_line.split("Intel Corporation ")[1].split(
                        " Integrated Graphics"
                    )[0]
                    # if there are no numbers, e.g. "Core Processor", tmp_model is not a model number
                    if not re.search("\\d+", tmp_model):
                        tmp_model = ""
                elif "HD Graphics" in first_line:
                    tmp_model = (
                        first_line.split("Intel Corporation ")[1]
                        .split("(", 1)[0]
                        .strip()
                    )
                elif "[" in first_line and "]" in first_line:
                    tmp_model = first_line.split("[")[1].split("]")[0]
                else:
                    tmp_model = ""

                if tmp_model != "":
                    gpu.model = tmp_model
                else:
                    gpu.model = ""

            # -----------------------------------------------------------------
            # VIA
            # -----------------------------------------------------------------
            elif first_line.startswith("VIA"):
                gpu.manufacturer_brand = "VIA"
                gpu.model = part_between_square_brackets

                tmp_model = first_line.split("[")[0]
                i = 0
                for i, char in enumerate("VIA Technologies, Inc. "):
                    if tmp_model[i] != char:
                        break
                gpu.internal_name = tmp_model[i:].strip()

            # -----------------------------------------------------------------
            # SiS
            # -----------------------------------------------------------------
            elif part_between_square_brackets == "SiS":
                # May be written somewhere else on other models, but we have so few SiS cards that it's difficult to
                # find more examples. Also, they haven't made any video card in the last 15 years or so.
                gpu.manufacturer_brand = part_between_square_brackets
                if gpu.reseller_brand.lower() == "silicon integrated systems":
                    gpu.reseller_brand = "SiS"
                gpu.model = first_line.split("]", 1)[1]
                # These may be useful for non-integrated cards, however the example ones are all integrated
                if " PCIE" in gpu.model:
                    gpu.model = gpu.model.split(" PCIE", 1)[0].strip()
                elif " PCI/AGP" in gpu.model:
                    gpu.model = gpu.model.split(" PCI/AGP", 1)[0].strip()
                if gpu.model in gpu.reseller_brand:
                    gpu.reseller_brand = gpu.reseller_brand.split(gpu.model, 1)[
                        0
                    ].strip()
            else:
                gpu.manufacturer_brand = None
                error = (
                    "I couldn't find the Video Card brand. The model was set to 'None' and is to be edited "
                    "logging into the TARALLO afterwards. The information you're looking for should be in the "
                    f"following 2 lines:\n{first_line}\n{second_line}\n"
                )
                if interactive:
                    print(error)
                gpu.warning += error

            if gpu.model is None:
                error = (
                    "I couldn't find the Integrated Graphics model. The model was set to 'None' and is to be "
                    "edited logging into the TARALLO afterwards. The information you're looking for should be in "
                    f"the following 2 lines:\n{first_line}\n{second_line}\n"
                )
                if interactive:
                    print(error)
                gpu.warning += error
            else:
                # Try to remove duplicate information
                gpu.reseller_brand = gpu.reseller_brand.replace(gpu.model, "").strip()

            if gpu.internal_name is not None:
                # Same
                gpu.reseller_brand = gpu.reseller_brand.replace(
                    gpu.internal_name, ""
                ).strip()

            break


def parse_glxinfo_output(gpu: VideoCard, glxinfo_path: str):
    try:
        with open(glxinfo_path, "r") as f:
            glxinfo_output = f.read()
    except FileNotFoundError:
        raise InputFileNotFoundError(glxinfo_path)

    for i, line in enumerate(glxinfo_output.splitlines()):

        # this line comes before the "Dedicated video memory" line
        # this basically saves a default value if the dedicated memory line cannot be found
        if "Video memory" in line:
            try:
                tmp_vid_mem = int(line.split(" ")[6].split(" ")[0][:-2])
                tmp_vid_mem_multiplier = line[-2:]
            except ValueError:
                exit(-1)
                return  # To stop complaints from PyCharm

            gpu.capacity = convert_video_memory_size(
                tmp_vid_mem, tmp_vid_mem_multiplier
            )

        if "Dedicated video memory" in line:
            try:
                tmp_vram = int(line.split(" ")[7].split(" ")[0])
                tmp_vram_multiplier = line[-2:]
            except ValueError:
                exit(-1)
                return
            capacity = convert_video_memory_size(tmp_vram, tmp_vram_multiplier)
            if capacity < 0:
                gpu.warning = "Could not find dedicated video memory"
                if gpu.capacity < 0:
                    gpu.warning += ". The value cannot be trusted."
            else:
                gpu.capacity = capacity
            break

    if gpu.capacity > 0:
        # Round to the next power of 2
        # this may be different from human readable capacity...
        rounded = 2 ** (gpu.capacity - 1).bit_length()
        one_and_half = int(rounded / 2 * 1.5)
        # Accounts for 3 GB VRAM cards and similar
        # Yes they do exist, try to remove this part and watch tests fail (and the card was manually verified to be 3 GB)
        if one_and_half >= gpu.capacity:
            gpu.capacity = one_and_half
        else:
            gpu.capacity = rounded


def convert_video_memory_size(capacity, units_of_measure):
    if units_of_measure == "GB":
        capacity *= 1024 * 1024 * 1024
    elif units_of_measure == "MB":
        capacity *= 1024 * 1024
    elif units_of_measure.upper() == "KB":
        capacity *= 1024
    else:
        capacity = -1

    return capacity


def read_lspci_and_glxinfo(
    has_dedicated: bool, lspci_path: str, glxinfo_path: str, interactive: bool = False
):
    gpu = VideoCard()
    if has_dedicated:
        parse_lspci_output(gpu, lspci_path, interactive)
        parse_glxinfo_output(gpu, glxinfo_path)
    else:  # integrated_in_mobo or integrated_in_cpu
        parse_lspci_output(gpu, lspci_path, interactive)
        # don't parse glxinfo because the VRAM is part of the RAM and varies
        gpu.capacity = None
        # print("The VRAM capacity could not be detected. "
        # "Please try looking for it on the Video Card or on the Internet. "
        # "The capacity value defaulted to 'None'. "
        # "For an integrated GPU, the VRAM may also be shared with the system RAM, so an empty value is acceptable.")

    result = {
        "type": "graphics-card",
        "brand": gpu.reseller_brand.strip(),
        "model": gpu.model.strip(),
        "internal-name": gpu.internal_name.strip(),
        "capacity-byte": gpu.capacity,
        "working": "yes",  # Indeed it is working
    }
    if gpu.manufacturer_brand is not None and gpu.reseller_brand is not None:
        if gpu.manufacturer_brand.lower() != gpu.reseller_brand.lower():
            result["brand-manufacturer"] = gpu.manufacturer_brand
    return result


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
        print(
            json.dumps(
                read_lspci_and_glxinfo(args.dedicated, args.lspci[0], args.glxinfo[0]),
                indent=2,
            )
        )
    except InputFileNotFoundError as e:
        print(str(e))
        exit(1)
