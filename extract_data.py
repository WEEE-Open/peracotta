#!/usr/bin/env python3

"""
Collect data from all the 'read...' scripts and returns it as a list of dicts
"""
import json

from InputFileNotFoundError import InputFileNotFoundError
from parsers.read_dmidecode import get_baseboard, get_chassis, get_connectors, get_net
from parsers.read_lscpu import read_lscpu
from parsers.read_decode_dimms import read_decode_dimms
from parsers.read_lspci_and_glxinfo import read_lspci_and_glxinfo
from parsers.read_smartctl import read_smartctl
from tarallo_token import TARALLO_TOKEN


def extract_and_collect_data_from_generated_files(directory: str, has_dedicated_gpu: bool, gpu_in_cpu: bool,
                                                  verbose: bool = False):
    directory = directory.rstrip('/')

    chassis, mobo, cpu, dimms, gpu, disks, psu = extract_data(directory, has_dedicated_gpu, gpu_in_cpu,
                                                              cleanup=False, verbose=verbose, unpack=False)

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

    wifi_cards = None
    if mobo.__len__() == 0:
        mobo = {
            "type": 'motherboard',
            "brand": None,
            "model": None,
            "serial_number": None
        }
    # in this case it contains wifi cards
    if isinstance(mobo, list):
        wifi_cards = []
        for wifi_card in mobo[1:]:
            wifi_cards.append(wifi_card)
        mobo = mobo[0]

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
    #TODO: normalization
    #TODO: check of keys for item
    #TODO: set new_format
    products = [chassis, mobo, cpu, gpu, psu]
    #setting mobo dict
    new_mobo = {"features": mobo, "contents": []}

    #mount the cpu
    new_mobo["contents"].append({"features": cpu})

    #adding some ram
    if isinstance(dimms, list):
        products += dimms
        for dimm in dimms:
            new_mobo["contents"].append({"features": dimm})
    else:
        new_mobo["contents"].append({"features": dimms}) #thanks to line 27 I know there's something, but it's not necessary.
        products.append(dimms)

    # mount disks
    if isinstance(disks, list):
        products += disks
        for disk in disks:
            new_mobo["contents"].append({"features": disk})
    elif isinstance(disks, dict) and disks.__len__() != 0:
        new_mobo["contents"].append({"features": disks})
        products.append(disks)

    #put gpu (still check if necessary 'null' format), assuming only one because was the same as before
    new_mobo["contents"].append({"features": gpu})

    #get wifi cards
    if wifi_cards:
        products += wifi_cards
        for wifi_card in wifi_cards:
            new_mobo["contents"].append({"features": wifi_card})

    #mounting psu (do I put in mobo or chassis?)
    new_mobo["contents"].append({"features": psu})

    #finally get the item
    result = [{"type": "I", "features": chassis, "contents": new_mobo}]

    # tuple = list(dicts), bool
    # result= chassis,mobo ,cpu, dimms, gpu, disks
    return result#, print_lspci_lines_in_dialog


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


# remove default/not found and human_readable values from TARALLO-ready JSON
def do_cleanup(result: list, verbose: bool = False) -> list:
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

        if verbose and len(removed) > 0:
            print(f"Removed from {item['type']}: {', '.join(removed)}.")

    # remove empty dicts
    filtered[:] = [item for item in filtered if item != {}]

    return filtered


def extract_data(directory: str, has_dedicated_gpu: bool, gpu_in_cpu: bool, cleanup: bool,
                 verbose: bool, unpack: bool = True):
    mobo = get_baseboard(directory + "/baseboard.txt")
    cpu = read_lscpu(directory + "/lscpu.txt")
    gpu = read_lspci_and_glxinfo(has_dedicated_gpu, directory + "/lspci.txt", directory + "/glxinfo.txt", verbose)
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
    mobo = get_connectors(directory + "/connector.txt", mobo, verbose)
    mobo = get_net(directory + "/net.txt", mobo, verbose)
    chassis = get_chassis(directory + "/chassis.txt")
    dimms = read_decode_dimms(directory + "/dimms.txt", verbose)
    if chassis["motherboard-form-factor"] == "proprietary-laptop":
        psu = {"type": "external-psu"}
    else:
        psu = {"type": "psu"}
    disks = read_smartctl(directory)

    result = []
    empty_dict = {}
    for component in (chassis, mobo, cpu, dimms, gpu, disks, psu):
        # return JSON ready for TARALLO
        if unpack:
            if isinstance(component, list):
                if component.__len__() == 0:
                    result.append(empty_dict)
                    continue
                for item in component:
                    result.append(item)
            else:
                result.append(component)
        # return list of lists of dicts to use in extract_and_collect_data_from_generated_files() for long output
        else:
            if component.__len__() == 0:
                result.append(empty_dict)
            else:
                result.append(component)

    if cleanup:
        result = do_cleanup(result, verbose)

    return result


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Parse the files generated with generate_files.sh and "
                                                 "get all the possible info out of them")
    gpu_group = parser.add_argument_group('GPU Location (one argument required)').add_mutually_exclusive_group(required=True)
    gpu_group.add_argument('-g', '--gpu', action="store_true", default=False, help="computer has dedicated GPU")
    gpu_group.add_argument('-c', '--cpu', action="store_true", default=False,
                           help="GPU is integrated inside the CPU")
    gpu_group.add_argument('-b', '--motherboard', action="store_true", default=False,
                           help="GPU is integrated inside the motherboard")
    gui_group = parser.add_argument_group('With or without GUI (one argument optional)').add_mutually_exclusive_group(required=False)
    gui_group.add_argument('-s', '--short', action="store_true", default=True,
                           help="enabled by default, this is the option you want if you want to copy-paste this "
                                "output into the TARALLO 'Bulk Add' page")
    gui_group.add_argument('-l', '--long', action="store_true", default=False, help="print longer output")
    gui_group.add_argument('-i', '--gui', action="store_true", default=False,
                           help="launch GUI instead of using the terminal version")
    parser.add_argument('-v', '--verbose', action="store_true", default=False, help="print some warning messages")
    parser.add_argument('path', action="store", nargs='?', type=str, help="path to directory with txt files generated "
                                                                          "by generate_files.sh - defaults to current "
                                                                          "directory")
    args = parser.parse_args()

    if args.path is None:
        path = "."
    else:
        path = args.path

    try:
        if args.long:
            data = extract_and_collect_data_from_generated_files(directory=path,
                                                                 has_dedicated_gpu=args.gpu,
                                                                 gpu_in_cpu=args.cpu,
                                                                 verbose=args.verbose)
            print(json.dumps(data, indent=2))

        elif args.gui:
            import main_with_gui
            main_with_gui.main()

        else:
            data = extract_data(directory=path,
                                has_dedicated_gpu=args.gpu,
                                gpu_in_cpu=args.cpu,
                                cleanup=True,
                                verbose=args.verbose)
            print(json.dumps(data, indent=2))

    except InputFileNotFoundError as e:
        print(str(e))
        exit(1)
