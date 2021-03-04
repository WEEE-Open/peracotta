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
                                                  verbose: bool = False, gui: bool = True):
    directory = directory.rstrip('/')

    chassis, mobo, cpu, dimms, gpu, disks, psu = extract_data(directory, has_dedicated_gpu, gpu_in_cpu,
                                                              gui=gui, verbose=verbose, unpack=False)
    # the None check MUST come before the others

    no_gpu_info_str = "I couldn't find the Video Card brand. The model was set to 'None' and is to be edited logging " \
                      "into the TARALLO afterwards. The information you're looking for should be in the following 2 lines:"
    no_vram_info_str = "A dedicated video memory couldn't be found. A generic video memory capacity was found instead, which " \
                       "could be near the actual value. Please humans, fix this error by hand."
    if len(chassis) == 0:
        chassis = {
            "type": "case",
            "brand": None,
            "model": None,
            "serial_number": None
        }

    wifi_cards = None
    if len(mobo) == 0:
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

    def is_product(component: dict):
        #check if brand and model exist
        if "brand" not in component.keys() or "model" not in component.keys():
            return False
        #check if brand or model has a not valid value
        candidates = [component["brand"].lower(), component["model"].lower()]
        for candidate in candidates:
            if isinstance(candidate, str) and candidate in ("", "null", "unknown", "undefined", "no enclosure"):
                return False
        #if all conditions are False, the product should be added
        return True


    def normalize_brands(coll_dict):
        names = {}
        with open("normalized.csv", "r") as f:
            for line in f.readlines():
                k, v = line.split(";", 2)[0:2]
                names[k] = v
        for p_dict in coll_dict:
            if "brand" in p_dict.keys():
                if p_dict["brand"] in names.keys():
                    p_dict["brand"] = names[p_dict["brand"]]

    item_keys = ["arrival-batch", "cib", "cib-old", "cib-qr", "data-erased", "mac", "notes",
                      "os-license-code", "os-license-version", "other-code", "owner", "smart-data",
                      "sn", "software", "surface-scan", "type", "working", "wwn"]
    bmv = ["brand", "model", "variant"]

    # search for a normalized form of brands for each component
    comp_wrap = []
    for component in (chassis, mobo, cpu, dimms, gpu, disks, psu):
        if isinstance(component, list):
            comp_wrap += component
        else:
            comp_wrap.append(component)
    normalize_brands(comp_wrap)

    products = []

    # setting mobo dict
    if is_product(mobo):
        products.append(mobo)
        new_mobo = {"features": {k: v for k, v in mobo.items() if k in bmv+item_keys},
                "contents": []}
    else:
        new_mobo = {"features": mobo, "contents": []}

    # mounting psu
    if len(psu) > 0:
        if is_product(psu):
            products.append(psu)
            psu = {"features": {k: v for k, v in psu.items() if k in bmv+item_keys}}
        else:
            psu = {"features": psu}

    #finally get the item
    if is_product(chassis):
        products.append(chassis)
        result = [{"type": "I", "features": {k: v for k, v in chassis.items() if k in bmv+item_keys},
                   "contents": [new_mobo, psu]}]
    else:
        result = [{"type": "I", "features": chassis, "contents": [new_mobo, psu]}]

    # mount the cpu
    if len(cpu) != 0:
        if isinstance(cpu, list):
            for one_cpu in cpu:
                if is_product(one_cpu):
                    products.append(one_cpu)
                    new_mobo["contents"].append({"features": {k: v for k, v in one_cpu.items() if k in bmv+item_keys}})
                else:
                    new_mobo["contents"].append({"features": one_cpu})
        else:
            if is_product(cpu):
                products.append(cpu)
                new_mobo["contents"].append({"features": {k: v for k, v in cpu.items() if k in bmv + item_keys}})
            else:
                new_mobo["contents"].append({"features": cpu})


    # adding some ram
    if isinstance(dimms, list):
        for dimm in dimms:
            if is_product(dimm):
                products.append(dimm)
                new_mobo["contents"].append({"features": {k: v for k, v in dimm.items() if k in bmv+item_keys}})
            else:
                new_mobo["contents"].append({"features": dimm})

    elif len(dimms) > 0:
        if is_product(dimms):
            products.append(dimms)
            new_mobo["contents"].append({"features": {k: v for k, v in dimms.items() if k in bmv+item_keys}})
        else:
            new_mobo["contents"].append({"features": dimms})

    # mount disks
    if isinstance(disks, list):
        for disk in disks:
            if is_product(disk):
                products.append(disk)
                result[0]["contents"].append({"features": {k: v for k, v in disk.items() if k in bmv+item_keys}})
            else:
                result[0]["contents"].append({"features": disk})

    elif isinstance(disks, dict) and disks != 0:
        if is_product(disks):
            products.append(disks)
            result[0]["contents"].append({"features": {k: v for k, v in disks.items() if k in bmv+item_keys}})
        else:
            result[0]["contents"].append({"features": disks})

    # put gpu (still check if necessary 'null' format), assuming only one because was the same as before
    if len(gpu) > 0:
        if is_product(gpu):
            products.append(gpu)
            new_mobo["contents"].append({"features": {k: v for k, v in gpu.items() if k in bmv+item_keys}})
        else:
            new_mobo["contents"].append({"features": gpu})

    # get wifi cards
    if wifi_cards and len(wifi_cards) > 0:
        for wifi_card in wifi_cards:
            if is_product(wifi_card):
                products.append(wifi_card)
                new_mobo["contents"].append({"features": {k: v for k, v in wifi_card.items() if k in bmv+item_keys}})
            else:
                new_mobo["contents"].append({"features": wifi_card})

    #fix the product type
    for product in products:
        #   create the dictionaries
        to_res = {k: product.pop(k) for k in bmv if k in product.keys()}
        to_res["type"] = "P"
        to_res["features"] = {k: v for k, v in product.items() if k not in item_keys}
        result.append(to_res)

    # tuple = list(dicts), bool
    # result= chassis,mobo ,cpu, dimms, gpu, disks
    return result


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
def do_cleanup(result: list, gui: bool, verbose: bool = False) -> list:
    filtered = []

    for item in result:
        removed = set()
        if isinstance(item, list):
            cleaned_item = do_cleanup(item, gui, verbose)
        else:
            cleaned_item = {}
            for k, v in item.items():
                if isinstance(v, str) and v == '':
                    removed.add(k)
                elif isinstance(v, int) and v <= 0:
                    removed.add(k)
                elif gui is False and 'human_readable' in k:
                    removed.add(k)
                else:
                    cleaned_item[k] = v
        filtered.append(cleaned_item)

        if verbose and len(removed) > 0:
            print(f"Removed from {item['type']}: {', '.join(removed)}.")

    # remove empty dicts
    #filtered[:] = [item for item in filtered """if item != {}"""]
    return filtered


def extract_data(directory: str, has_dedicated_gpu: bool, gpu_in_cpu: bool, gui: bool,
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

        result = do_cleanup(result, gui, verbose)

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
        if args.gui:
            import main_with_gui
            main_with_gui.main()

        else:
            data = extract_and_collect_data_from_generated_files(directory=path,
                                                                 has_dedicated_gpu=args.gpu,
                                                                 gpu_in_cpu=args.cpu,
                                                                 verbose=args.verbose,
                                                                 gui=False)
            print(json.dumps(data, indent=2))

    except InputFileNotFoundError as e:
        print(str(e))
        exit(1)
