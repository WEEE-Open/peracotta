#!/usr/bin/env python3

"""
Collect data from all the 'read...' scripts and returns it as a list of dicts
"""
import json
import os
import fnmatch
import random
from datetime import datetime
from pytarallo import Tarallo
from pytarallo.Errors import NoInternetConnectionError
from dotenv import load_dotenv
from os import environ as env

from rich import print
from rich.console import Console
from rich import traceback

from InputFileNotFoundError import InputFileNotFoundError
from parsers.read_dmidecode import get_baseboard, get_chassis, get_connectors, get_net
from parsers.read_lscpu import read_lscpu
from parsers.read_decode_dimms import read_decode_dimms
from parsers.read_lspci_and_glxinfo import read_lspci_and_glxinfo
from parsers.read_smartctl import read_smartctl

traceback.install()


def is_product(component: dict):
    # check if brand and model exist
    if "brand" not in component or "model" not in component:
        return False
    # check if brand or model has a not valid value
    candidates = [component["brand"].lower(), component["model"].lower()]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.lower() in (
            "",
            "null",
            "unknown",
            "undefined",
            "no enclosure",
            "to be filled by o.e.m.",
        ):
            return False
    # if all conditions are False, the product should be added
    return True


def extract_and_collect_data_from_generated_files(
    directory: str,
    has_dedicated_gpu: bool,
    gpu_in_cpu: bool,
    verbose: bool = False,
    gui: bool = True,
):
    directory = directory.rstrip("/")

    chassis, mobo, cpu, dimms, gpu, disks, psu = extract_data(
        directory, has_dedicated_gpu, gpu_in_cpu, gui=gui, verbose=verbose, unpack=False
    )
    # the None check MUST come before the others

    no_gpu_info_str = (
        "I couldn't find the Video Card brand. The model was set to 'None' and is to be edited logging "
        "into the TARALLO afterwards. The information you're looking for should be in the following 2 lines:"
    )
    no_vram_info_str = (
        "A dedicated video memory couldn't be found. A generic video memory capacity was found instead, which "
        "could be near the actual value. Please humans, fix this error by hand."
    )
    if len(chassis) == 0:
        chassis = {"type": "case", "brand": None, "model": None, "serial_number": None}

    wifi_cards = None
    if len(mobo) == 0:
        mobo = {
            "type": "motherboard",
            "brand": None,
            "model": None,
            "serial_number": None,
        }
    # in this case it contains wifi cards
    if isinstance(mobo, list):
        wifi_cards = []
        for wifi_card in mobo[1:]:
            wifi_cards.append(wifi_card)
        mobo = mobo[0]

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

    item_keys = [
        "arrival-batch",
        "cib",
        "cib-old",
        "cib-qr",
        "data-erased",
        "mac",
        "notes",
        "os-license-code",
        "os-license-version",
        "other-code",
        "owner",
        "smart-data",
        "sn",
        "software",
        "surface-scan",
        "working",
        "wwn",
    ]
    both = ["brand", "model", "variant", "type"]

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
        new_mobo = {
            "features": {k: v for k, v in mobo.items() if k in both + item_keys},
            "contents": [],
        }
    else:
        new_mobo = {"features": mobo, "contents": []}

    # mounting psu
    if len(psu) > 0:
        if is_product(psu):
            products.append(psu)
            psu = {"features": {k: v for k, v in psu.items() if k in both + item_keys}}
        else:
            psu = {"features": psu}

    # finally get the item
    if is_product(chassis):
        products.append(chassis)
        new_chassis = {
            "type": "I",
            "features": {k: v for k, v in chassis.items() if k in both + item_keys},
            "contents": [new_mobo, psu],
        }
    else:
        new_chassis = {"type": "I", "features": chassis, "contents": [new_mobo, psu]}

    result = [new_chassis]

    # mount the cpu
    if len(cpu) > 0:
        if isinstance(cpu, list):
            for one_cpu in cpu:
                if len(one_cpu) > 0:
                    if is_product(one_cpu):
                        products.append(one_cpu)
                        new_mobo["contents"].append(
                            {
                                "features": {
                                    k: v
                                    for k, v in one_cpu.items()
                                    if k in both + item_keys
                                }
                            }
                        )
                    else:
                        new_mobo["contents"].append({"features": one_cpu})
        else:
            if len(cpu) > 0 and is_product(cpu):
                products.append(cpu)
                new_mobo["contents"].append(
                    {
                        "features": {
                            k: v for k, v in cpu.items() if k in both + item_keys
                        }
                    }
                )
            elif len(cpu) > 0:
                new_mobo["contents"].append({"features": cpu})

    # adding some ram
    if isinstance(dimms, list):
        for dimm in dimms:
            if len(dimm) > 0:
                if len(dimm) > 0 and is_product(dimm):
                    products.append(dimm)
                    new_mobo["contents"].append(
                        {
                            "features": {
                                k: v for k, v in dimm.items() if k in both + item_keys
                            }
                        }
                    )
                else:
                    new_mobo["contents"].append({"features": dimm})

    elif len(dimms) > 0:
        if is_product(dimms):
            products.append(dimms)
            new_mobo["contents"].append(
                {"features": {k: v for k, v in dimms.items() if k in both + item_keys}}
            )
        else:
            new_mobo["contents"].append({"features": dimms})

    # mount disks
    if isinstance(disks, list):
        for disk in disks:
            if len(disk) > 0:
                if is_product(disk):
                    products.append(disk)
                    new_chassis["contents"].append(
                        {
                            "features": {
                                k: v for k, v in disk.items() if k in both + item_keys
                            }
                        }
                    )
                else:
                    new_chassis["contents"].append({"features": disk})

    elif isinstance(disks, dict) and len(disks) > 0:
        if is_product(disks):
            products.append(disks)
            new_chassis["contents"].append(
                {"features": {k: v for k, v in disks.items() if k in both + item_keys}}
            )
        else:
            new_chassis["contents"].append({"features": disks})

    # put gpu (still check if necessary 'null' format), assuming only one because was the same as before
    if len(gpu) > 0:
        if is_product(gpu):
            products.append(gpu)
            new_mobo["contents"].append(
                {"features": {k: v for k, v in gpu.items() if k in both + item_keys}}
            )
        else:
            new_mobo["contents"].append({"features": gpu})

    # get wifi cards
    if wifi_cards and len(wifi_cards) > 0:
        for wifi_card in wifi_cards:
            if len(wifi_card) > 0:
                if is_product(wifi_card):
                    products.append(wifi_card)
                    new_mobo["contents"].append(
                        {
                            "features": {
                                k: v
                                for k, v in wifi_card.items()
                                if k in both + item_keys
                            }
                        }
                    )
                else:
                    new_mobo["contents"].append({"features": wifi_card})

    # fix the product type
    for product in products:
        #   create the dictionaries
        to_res = {
            k: product.pop(k) for k in both if k in product.keys() and k != "type"
        }
        to_res["type"] = "P"
        to_res["features"] = {
            k: v for k, v in product.items() if k not in item_keys or k == "type"
        }
        if to_res not in result:
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
        model = gpu["model"]
    elif internal_name_present:
        model = gpu["internal-name"]
    else:
        model = None

    result = {}
    if brand is not None:
        result["integrated-graphics-brand"] = brand
    if model is not None:
        result["integrated-graphics-model"] = model
    return result


# remove default/not found values from TARALLO-ready JSON
def do_cleanup(result: list, gui: bool, verbose: bool = False) -> list:
    filtered = []

    for item in result:
        removed = set()
        if isinstance(item, list):
            cleaned_item = do_cleanup(item, gui, verbose)
        else:
            cleaned_item = {}
            for k, v in item.items():
                if isinstance(v, str) and v == "":
                    removed.add(k)
                elif isinstance(v, int) and v <= 0:
                    removed.add(k)
                elif v is None:
                    removed.add(k)
                else:
                    cleaned_item[k] = v
        filtered.append(cleaned_item)

        if verbose and len(removed) > 0:
            print(f"Removed from {item['type']}: {', '.join(removed)}.")

    # remove empty dicts
    # filtered[:] = [item for item in filtered """if item != {}"""]
    return filtered


def extract_data(
    directory: str,
    has_dedicated_gpu: bool,
    gpu_in_cpu: bool,
    gui: bool,
    verbose: bool,
    unpack: bool = True,
):
    mobo = get_baseboard(directory + "/baseboard.txt")
    cpu = read_lscpu(directory + "/lscpu.txt")
    gpu = read_lspci_and_glxinfo(
        has_dedicated_gpu, directory + "/lspci.txt", directory + "/glxinfo.txt", verbose
    )
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
                if len(component) == 0:
                    result.append(empty_dict)
                    continue
                for item in component:
                    result.append(item)
            else:
                result.append(component)
        # return list of lists of dicts to use in extract_and_collect_data_from_generated_files() for long output
        else:
            if len(component) == 0:
                result.append(empty_dict)
            else:
                result.append(component)

        result = do_cleanup(result, gui, verbose)

    # check on case and mobo
    try:
        if (chassis["model"], chassis["brand"], chassis["variant"]) == (
            mobo["brand"],
            mobo["model"],
            mobo["variant"],
        ):
            chassis.pop("model")
    except KeyError:
        pass

    # maybe there's a nicer way
    comparator = []
    for comp in result:
        if isinstance(comp, list):
            comparator = comparator + comp
        else:
            comparator.append(comp)

    # avoid bad associations between items and products
    for comp1 in comparator:
        for comp2 in comparator:
            if (
                is_product(comp1)
                and is_product(comp2)
                and comp1["type"] != comp2["type"]
            ):
                if (comp1["brand"], comp2["model"]) == (comp2["brand"], comp2["model"]):
                    variant1 = comp1.pop("variant", "")
                    variant2 = comp2.pop("variant", "")
                    if variant1 == variant2:
                        comp1["variant"] = variant1.rstrip().join(f"_{comp1['type']}")
                        comp2["variant"] = variant2.rstrip().join(f"_{comp2['type']}")
    return result


def get_gpu(args):
    if args.files is not None:
        args.cpu = False
        args.gpu = False
        args.motherboard = False

        try:
            with open(os.path.join(os.getcwd(), args.files, "gpu_location.txt")) as f:
                location = f.readline().lower().rstrip()
                if location == "mobo":
                    args.motherboard = True
                elif location == "gpu":
                    args.gpu = True
                elif location == "cpu":
                    args.cpu = True
        except FileNotFoundError:
            pass

    while not any((args.gpu, args.cpu, args.motherboard)):
        print(
            "\nWhere is GPU in your PC? c/g/b\n",
            "c for integrated in CPU\n",
            "g for discrete graphics card\n",
            "b for integrated in the motherboard\n",
        )
        gpu_flag = input("Insert your choice: ")
        if gpu_flag == "c":
            args.cpu = True
        elif gpu_flag == "g":
            args.gpu = True
        elif gpu_flag == "b":
            args.motherboard = True
    return args.cpu, args.gpu, args.motherboard


def print_output(output, path):
    print(
        "\nThe following output can be copy-pasted into the 'Bulk Add' page of the TARALLO, from '[' to ']':\n"
    )
    print(output)

    with open(os.path.join(path, "copy_this_to_tarallo.json"), "w") as f:
        f.write(output)

    print(
        f"You can also transfer the generated JSON file $OUTPUT_PATH/copy_this_to_tarallo.json to your PC with 'scp {path}/copy_this_to_tarallo.json <user>@<your_PC's_IP>:/path/on/your/PC' right from this terminal."
    )


def run_extract_data(path, args):
    try:
        data = extract_and_collect_data_from_generated_files(
            directory=path,
            has_dedicated_gpu=args.gpu,
            gpu_in_cpu=args.cpu,
            verbose=args.verbose,
            gui=False,
        )
    except InputFileNotFoundError as e:
        print(str(e))
        exit(1)
    return data


def check_required_files(path):
    file_in_dir = os.listdir(path)
    with open("required_files.txt", "r") as f:
        for line in f.readlines():
            file = line.rstrip()

            for ex in file_in_dir:
                if fnmatch.fnmatch(ex, file):
                    break
            else:
                print(
                    f"[bold red]Missing file {file}\nPlease re-run this script without the -f or --files option.[/]"
                )
                exit(-1)


def check_and_install_dependencies():
    install_cmd = "apt install -y pciutils i2c-tools mesa-utils smartmontools dmidecode < /dev/null"
    exit_value = os.system(
        "dpkg -s pciutils i2c-tools mesa-utils smartmontools dmidecode > /dev/null"
    )
    if exit_value == 1:
        ans = input(
            "You need to install some packages in order for the peracotta to work. Do you want to install them? y/N "
        ).lower()
        if ans == "y":
            if os.geteuid() != 0:
                os.system(f"sudo {install_cmd}")
            else:
                os.system(f"/bin/bash/ -c {install_cmd}")
        else:
            print("[blue]Quitting...[/]")
            exit(-1)


def prompt_to_open_browser():
    import base64

    web_link = "aHR0cHM6Ly90YXJhbGxvLndlZWVvcGVuLml0L2J1bGsvYWRkCg=="
    web_link = base64.b64decode(web_link).decode("ascii").rstrip()
    egg = Console()
    text = [
        "Congratulations!!!",
        "You're",
        "the",
        "1000th",
        "WEEEisitor",
        "of",
        "the",
        "day",
    ]
    this_moment = datetime.now()
    if this_moment.minute == this_moment.second:
        for word in text:
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            egg.print(word, end=" ", style=f"rgb({red},{green},{blue})")
        egg.print(web_link)
    else:
        print(
            f"[green]Finished successfully![/] Now you can add this output to the T.A.R.A.L.L.O. -> {web_link}"
        )


def get_additional_info(gathered_data):
    code = input("Does this have a code already? (optional, ENTER to skip): ")
    if code:
        # some elaboration just to let in the upper part the 'code' key. Not necessary but definitely better looking
        new = {'code': code}
        new.update(gathered_data[0])
        gathered_data[0] = new

    owner = input("Do you want to add a owner? (optional, ENTER to skip): ")
    if owner:
        gathered_data[0]['features']['owner'] = owner


def upload(jsoned):
    msg_upload_ok = "[green]All went fine! [/] [blue]\nBye bye! [/]🍐\n"
    msg_upload_failed = "The upload failed. Check above and try to upload on your own"

    ans = (
        input(
            "Do you want to automatically upload the JSON to the T.A.R.A.L.L.O ? (Y/n): "
        )
        .lower()
        .rstrip()
    )

    if ans.lower() == "n":
        print("\n[blue]Bye bye! [/]🍐\n")

        return

    try:
        load_dotenv()
        t_url = env["TARALLO_URL"]
        t_token = env["TARALLO_TOKEN"]
    except KeyError:

        raise EnvironmentError(
            "Missing definitions of TARALLO* environment variables (see the README)"
        )

    while True:
        try:
            bulk_id = input("Please enter a bulk identifier (optional): ").rstrip()
            t = Tarallo.Tarallo(t_url, t_token)
            ver = t.bulk_add(jsoned, bulk_id, False)
            if ver:
                print(msg_upload_ok)
                break
            else:

                overwrite = (
                    input(
                        "Cannot update, do you want to try overwriting the identifier? (y/N): "
                    )
                    .lower()
                    .rstrip()
                )
                if overwrite.lower() == "y":

                    ver = t.bulk_add(jsoned, bulk_id, True)
                    if ver:
                        print(msg_upload_ok)
                        break
                    else:
                        print(msg_upload_failed)
                else:
                    bulk_id = input(
                        "Do you want to use another identifier? Just press enter for an automatic one. "
                        "You choose (NEW_ID/n): "
                    ).rstrip()
                    if bulk_id.lower() != "n":
                        ver = t.bulk_add(jsoned, bulk_id, True)
                        if ver:
                            print(msg_upload_ok)
                            break
                        else:
                            print(msg_upload_failed)

        except NoInternetConnectionError:
            print(
                "\n[yellow]Unable to reach the T.A.R.A.L.L.O. "
                "Please connect this PC to the Internet and try again.[/]\n"
            )


def main(args):
    path = os.getcwd()

    if args.gui:
        import main_with_gui

        main_with_gui.main()

    elif args.files is not None:
        # if -f flag is added, most of the other flags doesn't mean anything
        if args.path is not None or any((args.cpu, args.gpu, args.motherboard)):
            print(
                "[bold red]Error: Bad flags combination (./main.py -f <path> is correct) [/]"
            )
            exit(-1)
        path = os.path.join(path, args.files)
        check_required_files(path)
        args.cpu, args.gpu, args.motherboard = get_gpu(args)

    else:
        if args.path is None:
            path = os.path.join(path, "tmp")
            if os.path.isdir(path):
                sel = input("Overwrite existing files in tmp dir? y/N ").lower()
                if sel == "y":
                    print("Overwriting...")
                else:
                    sel = input("Output files to working directory? y/N ").lower()
                    if sel == "y":
                        path = os.getcwd()
                        print("Outputting files to working directory...")
                    else:
                        print("[blue]Quitting...[/]")
                        exit(-1)
            else:
                os.mkdir(path)

        else:
            path = os.path.join(path, args.path)
            if os.path.isdir(path):
                print(
                    "[bold red]Wrong path: can't create a directory with this name, existing already[/]"
                )
                exit(-2)
            os.mkdir(path)
        check_and_install_dependencies()

        # now that I have a dest folder, I generate files
        if os.geteuid() != 0:
            os.system(f"sudo ./scripts/generate_files.sh {path}")
        else:
            os.system(f"./scripts/generate_files.sh {path}")

        # file generated, extract data next
        args.cpu, args.gpu, args.motherboard = get_gpu(args)

    final_output = run_extract_data(path, args)
    get_additional_info(final_output)
    print_output(json.dumps(final_output, indent=2), path)
    prompt_to_open_browser()
    upload(final_output)


def generate_parser():

    import argparse

    parser = argparse.ArgumentParser(
        description="Parse the files generated with generate_files.sh and "
        "get all the possible info out of them",
        epilog="If no argument is given, then this script will interactively guide you to run the PERACOTTA data gathering package."
        "Alternatively, you can choose to pass either the path to the directory where you want the files to be generated, the gpu location, or both."
        "In this case, the script will only become interactive when needed, and it won't ask you anything if you pass both the path and the gpu location.",
    )
    parser.add_argument(
        "-f",
        "--files",
        action="store",
        default=None,
        required=False,
        help="retrieve previously generated files from a given path",
    )
    gpu_group = parser.add_argument_group("GPU Location").add_mutually_exclusive_group(
        required=False
    )
    gpu_group.add_argument(
        "-g",
        "--gpu",
        action="store_true",
        default=False,
        help="computer has dedicated GPU",
    )
    gpu_group.add_argument(
        "-c",
        "--cpu",
        action="store_true",
        default=False,
        help="GPU is integrated inside the CPU",
    )
    gpu_group.add_argument(
        "-b",
        "--motherboard",
        action="store_true",
        default=False,
        help="GPU is integrated inside the motherboard",
    )
    gui_group = parser.add_argument_group(
        "With or without GUI (one argument optional)"
    ).add_mutually_exclusive_group(required=False)
    gui_group.add_argument(
        "-i",
        "--gui",
        action="store_true",
        default=False,
        help="launch GUI instead of using the terminal version",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="print some warning messages",
    )
    parser.add_argument(
        "path",
        action="store",
        nargs="?",
        type=str,
        help="optional path where generated files are stored",
    )

    return parser


if __name__ == "__main__":
    args = generate_parser().parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print("\n[blue]Quitting...[/]")
