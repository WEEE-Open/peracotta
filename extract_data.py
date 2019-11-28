#!/usr/bin/env python3

"""
Collect data from all the 'read...' scripts and returns it as a list of dicts
"""
import json

from InputFileNotFoundError import InputFileNotFoundError
from read_dmidecode import get_baseboard, get_chassis, get_connectors, get_net
from read_lscpu import read_lscpu
from read_decode_dimms import read_decode_dimms
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_smartctl import read_smartctl
from tarallo_token import TARALLO_TOKEN


def extract_and_collect_data_from_generated_files(directory: str, has_dedicated_gpu: bool, gpu_in_cpu: bool,
                                                  interactive: bool = False):
    directory = directory.rstrip('/')

    chassis, mobo, cpu, dimms, gpu, disks, psu = extract_data(directory, has_dedicated_gpu, gpu_in_cpu, False,
                                                              interactive)

    # TODO: add mobo, chassis, cpu, disks checks

    no_dimms_str = "decode-dimms was not able to find any RAM details"

    # the None check MUST come before the others
    if dimms.__len__() == 0:
        # empty default dictionary
        dimms = {
            "type": "ram",
            "working": "yes",
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

    no_gpu_info_str = "I couldn't find the Video Card brand. The model was set to 'None' and is to be edited logging " \
                      "into the TARALLO afterwards. The information you're looking for should be in the following 2 lines:"
    no_vram_info_str = "A dedicated video memory couldn't be found. A generic video memory capacity was found instead, which " \
                       "could be near the actual value. Please humans, fix this error by hand."

    if gpu.__len__() == 0 or (no_gpu_info_str in gpu and no_vram_info_str in gpu):
        gpu = {
            "type": "graphics-card",
            "manufacturer_brand": None,
            "reseller_brand": None,
            "model": None,
            "capacity": None,
            "human_readable_capacity": None
        }
        print_lspci_lines_in_dialog = True

    elif no_vram_info_str in gpu and no_gpu_info_str not in gpu:
        # TODO: check output in this case, change only VRAM field to None
        print_lspci_lines_in_dialog = False
    else:
        print_lspci_lines_in_dialog = False

    if chassis.__len__() == 0:
        chassis = {
            "type": "case",
            "brand": None,
            "model": None,
            "serial_number": None
        }
    if mobo.__len__() == 0:
        mobo = {
            "type": 'motherboard',
            "brand": None,
            "model": None,
            "serial_number": None
        }

    if cpu.__len__() == 0:
        cpu = {
            "type": "cpu",
            "isa": None,
            "model": None,
            "brand": None,
            "core-n": None,
            "thread-n": None,
            "frequency-hertz": None,
            "human_readable_frequency": None
        }

    result = [chassis, mobo, cpu]

    if isinstance(dimms, dict):
        # otherwise it will append every key-value pair of the dict
        result.append(dimms)
    else:
        for dimm in dimms:
            result.append(dimm)

    # assuming there is only 1 graphics card in the system
    result.append(gpu)

    if isinstance(disks, dict):
        result.append(disks)
    else:
        for disk in disks:
            result.append(disk)

    # tuple = list(dicts), bool
    return result, print_lspci_lines_in_dialog


def extract_integrated_gpu_from_standalone(gpu: dict) -> dict:
    if "brand-manufacturer" in gpu and len("brand-manufacturer") > 0:
        brand = gpu["brand-manufacturer"]
    elif "brand" in gpu and len("brand") > 0:
        brand = gpu["brand"]
    else:
        brand = None

    internal_name_present = len(gpu["internal-name"]) > 0
    model_present = len(gpu["model"]) > 0
    if model_present and internal_name_present:
        model = f"{gpu['model']} ({gpu['internal-name']})"
    elif model_present:
        model = gpu['model']
    elif internal_name_present:
        model = gpu['internal-name']
    else:
        model = None

    result = {}
    if brand is not None:
        result["integrated-graphics-brand"] = brand
    if model is not None:
        result["integrated-graphics-model"] = model
    return result


def do_cleanup(result: list, interactive: bool = False) -> list:
    filtered = []

    for item in result:
        cleaned_item = {}
        removed = set()
        for k, v in item.items():
            if isinstance(v, str) and v == '':
                removed.add(k)
            elif isinstance(v, int) and v <= 0:
                removed.add(k)
            elif 'human_readable' in k:
                removed.add(k)
            else:
                cleaned_item[k] = v
        filtered.append(cleaned_item)

        if interactive and len(removed) > 0:
            print(f"Removed from {item['type']}: {', '.join(removed)}.")
    return filtered


def extract_data(directory: str, has_dedicated_gpu: bool, gpu_in_cpu: bool, cleanup: bool, interactive: bool) -> dict:
    mobo = get_baseboard(directory + "/baseboard.txt")
    cpu = read_lscpu(directory + "/lscpu.txt")
    gpu = read_lspci_and_glxinfo(has_dedicated_gpu, directory + "/lspci.txt", directory + "/glxinfo.txt", interactive)
    if not has_dedicated_gpu:
        entries = extract_integrated_gpu_from_standalone(gpu)
        if gpu_in_cpu:
            if isinstance(cpu, list):
                # Multiple processors
                updated_cpus = []
                for one_cpu in cpu:
                    one_cpu = {**one_cpu, **entries}
                    updated_cpus.append(one_cpu)
                cpu = updated_cpus
                del updated_cpus
            else:
                cpu = {**cpu, **entries}
        else:
            mobo = {**mobo, **entries}
        gpu = []
    mobo = get_connectors(directory + "/connector.txt", mobo, interactive)
    mobo = get_net(directory + "/net.txt", mobo, interactive)
    chassis = get_chassis(directory + "/chassis.txt")
    dimms = read_decode_dimms(directory + "/dimms.txt", interactive)
    if chassis["motherboard-form-factor"] == "proprietary-laptop":
        psu = {"type": "external-psu"}
    else:
        psu = {"type": "psu"}
    disks = read_smartctl(directory)

    result = []
    empty_dict = {}
    for thing in (chassis, mobo, cpu, dimms, gpu, disks, psu):
        if thing.__len__() == 0:
            result.append(empty_dict)
        else:
            result.append(thing)
    if cleanup:
        result = do_cleanup(result, interactive)

    return result


if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Get all the possible output data things")
    parser.add_argument('-l', '--long', action="store_true", default=False, help="print longer output")
    # TODO: add option to launch GUI
    group = parser.add_argument_group('GPU Location').add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--gpu', action="store_true", default=False, help="computer has dedicated GPU")
    group.add_argument('-c', '--cpu', action="store_true", default=False,
                        help="GPU is integrated inside the CPU")
    group.add_argument('-b', '--motherboard', action="store_true", default=False,
                        help="GPU is integrated inside the motherboard")
    parser.add_argument('-v', '--verbose', action="store_true", default=False, help="print some warning messages")
    parser.add_argument('path', action="store", nargs='?', type=str, help="to directory with txt files")
    args = parser.parse_args()

    if args.path is None:
        if not os.path.isdir("tmp"):
            os.makedirs("tmp")
        else:
            path = "tmp"
    else:
        path = args.path

    try:
        if args.long:
            data = extract_data(path, args.gpu, args.cpu, True, args.verbose)
            print(json.dumps(data, indent=2))
        else:
            print(json.dumps(extract_and_collect_data_from_generated_files(path, args.gpu, args.cpu, args.verbose),
                             indent=2))
    except InputFileNotFoundError as e:
        print(str(e))
        exit(1)

