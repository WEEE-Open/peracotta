#!/bin/usr/python3

"""
Collect data from all the 'read...' scripts and returns it as a list of dicts
"""

from read_dmidecode import get_baseboard, get_chassis
from read_lscpu import read_lscpu
from read_decode_dimms import read_decode_dimms
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_smartctl import read_smartctl


def extract_and_collect_data_from_generated_files(has_dedicated_gpu: bool):

    # TODO: reset to tmp after testing
    # this is set in generate_files.sh and main_with_gui.py and has to be changed manually
    # directory = "tmp"
    directory = "tests/castes-pc"

    mobo = get_baseboard(directory + "/baseboard.txt")
    cpu = read_lscpu(directory + "/lscpu.txt")
    chassis = get_chassis(directory + "/chassis.txt")
    dimms = read_decode_dimms(directory + "/dimms.txt")
    lspci_glxinfo = read_lspci_and_glxinfo(has_dedicated_gpu, directory + "/lspci.txt", directory + "/glxinfo.txt")
    disks = read_smartctl(directory)

    # TODO: add mobo, chassis, cpu, disks checks

    no_dimms_str = "decode-dimms was not able to find any RAM details"

    # the None check MUST come before the others
    if dimms is None or no_dimms_str in dimms:
        # empty default dictionary
        dimms = {
            "type": "ram",
            "brand": None,
            "model": None,
            "serial_number": None,
            "frequency": None,
            "human_readable_frequency": None,
            "capacity": None,
            "human_readable_capacity": None,
            "RAM_type": None,
            "ECC": None
            # "CAS_latencies": None # feature missing from TARALLO
        }

    no_gpu_info_str = "I couldn't find the Video Card brand. The model was set to 'None' and is to be edited logging into " \
                  "the TARALLO afterwards. The information you're looking for should be in the following 2 lines:"
    no_vram_info_str = "A dedicated video memory couldn't be found. A generic video memory capacity was found instead, which " \
                  "could be near the actual value. Please humans, fix this error by hand."

    if lspci_glxinfo is None or (no_gpu_info_str in lspci_glxinfo and no_vram_info_str in lspci_glxinfo):
        lspci_glxinfo = {
            "type": "graphics-card",
            "manufacturer_brand": None,
            "reseller_brand": None,
            "model": None,
            "capacity": None,
            "human_readable_capacity": None
        }
        print_lspci_lines_in_dialog = True

    elif no_vram_info_str in lspci_glxinfo and not no_gpu_info_str in lspci_glxinfo:
        # TODO: check output in this case, change only VRAM field to None
        print_lspci_lines_in_dialog = False

    else:
        print_lspci_lines_in_dialog = False


    result = []

    result.append(chassis)

    result.append(mobo)

    result.append(cpu)

    if isinstance(dimms, dict):
        # otherwise it will append every key-value pair of the dict
        result.append(dimms)
    else:
        for dimm in dimms:
            result.append(dimm)

    # assuming there is only 1 graphics card in the system
    result.append(lspci_glxinfo)

    if isinstance(disks, dict):
        result.append(disks)
    else:
        for disk in disks:
            result.append(disk)

    # tuple = list(dicts), bool
    return result, print_lspci_lines_in_dialog


if __name__ == '__main__':
    # TODO: refactor after testing
    # extract_and_collect_data_from_generated_files()
    print(extract_and_collect_data_from_generated_files(True))