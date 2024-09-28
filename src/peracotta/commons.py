#!/usr/bin/env python3
import copy
import os
import subprocess
import sys
from enum import Enum
from typing import List, Optional, Set

from .constants import basedir
from .parsers import parse_case, parse_decode_dimms, parse_lscpu, parse_lspci_and_glxinfo, parse_motherboard, parse_psu, parse_smartctl, parse_udevadm


class InputFileNotFoundError(FileNotFoundError):
    def __init__(self, path):
        super().__init__(f"Cannot open file {path}")
        self.path = path

    def get_path(self):
        return self.path


class GenerateFilesError(BaseException):
    def __init__(self, msg):
        super().__init__(msg)


class SudoError(GenerateFilesError):
    def __init__(self, msg):
        super().__init__(msg)


MEANINGLESS_VALUES = (
    "",
    "null",
    "custom",
    "unknown",
    "undefined",
    "no enclosure",
    "not available",
    "chassis manufacture",
    "chassis serial number",
    "to be filled by o.e.m",
    "to be filled by o.e.m.",
)


class GpuLocation(Enum):
    NONE = 0
    DISCRETE = 1
    CPU = 2
    MOTHERBOARD = 3


class ParserComponents(Enum):
    CASE = "Case"
    MOTHERBOARD = "Motherboard"
    CPU = "CPU"
    RAM = "RAM"
    GPU = "GPU"
    HDD = "HDD"
    SSD = "SSD"
    PSU = "Power supply"
    ODD = "ODD"
    MONITOR = "Monitor"
    INPUT = "Input devices"

    @classmethod
    def all(cls):
        return list(cls)

    @classmethod
    def all_names(cls):
        res = []
        for thing in cls:
            res.append(thing.value)
        return res

    @classmethod
    def all_keys(cls):
        res = []
        for thing in cls:
            res.append(thing.name)
        return res

    @classmethod
    def not_implemented_yet(cls):
        return {
            ParserComponents.ODD,
            ParserComponents.MONITOR,
            ParserComponents.INPUT,
        }


def check_dependencies_for_generate_files():
    retval = os.system("dpkg -s pciutils i2c-tools mesa-utils smartmontools dmidecode > /dev/null")
    return retval == 0


def generate_files(path: str, use_sudo: bool = True, sudo_passwd: str = None):
    if os.path.exists(os.path.join(basedir, "scripts/generate_files.pxec")):
        script = "scripts/generate_files.pkexec"
    else:
        script = "scripts/generate_files.sh"
    script = os.path.join(basedir, script)
    os.makedirs(path, exist_ok=True)
    command = [script, path]
    if use_sudo:
        command = ["sudo", "-S"] + command

    p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    if sudo_passwd is not None:
        try:
            # out, err =
            p.communicate(input=(sudo_passwd + "\n").encode(), timeout=30)
        except subprocess.TimeoutExpired:
            p.kill()
            raise GenerateFilesError(" ".join(command) + " timed out after 30 seconds")
    else:
        try:
            p.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            p.kill()
            raise GenerateFilesError(" ".join(command) + " timed out after 30 seconds")

    if p.returncode is None:
        raise GenerateFilesError(" ".join(command) + " did not run")
    elif p.returncode != 0:
        if use_sudo and p.returncode == 1:
            raise SudoError(" ".join(command) + f" failed, return code: {p.returncode}")
        else:
            raise GenerateFilesError(" ".join(command) + f" failed, return code: {p.returncode}")

    return path


def required_files():
    return (
        "baseboard.txt",
        "chassis.txt",
        "connector.txt",
        "dimms.txt",
        "glxinfo.txt",
        "lscpu.txt",
        "lspci.txt",
        "net.txt",
        "smartctl.txt",
    )


def _merge_gpu(current_results: List[dict], target_type: str, gpus: list) -> None:
    if len(gpus) <= 0:
        return
    features = _extract_gpu_for_integrated(gpus[0])

    for target in _find_all_components(target_type, current_results):
        target.update(features)


def _extract_gpu_for_integrated(gpu: dict) -> dict:
    if "brand-manufacturer" in gpu and len("brand-manufacturer") > 0:
        brand = gpu["brand-manufacturer"]
    elif "brand" in gpu and len("brand") > 0:
        brand = gpu["brand"]
    else:
        brand = None

    internal_name_present = "internal-name" in gpu
    model_present = "model" in gpu
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


def _find_component(component_type: str, result: List[dict]) -> Optional[dict]:
    for component in result:
        if "type" in component and component["type"] == component_type:
            return component
    return None


def _find_all_components(component_type: str, result: List[dict]) -> List[dict]:
    return_this = []
    for component in result:
        if "type" in component and component["type"] == component_type:
            return_this.append(component)
    return return_this


def call_parsers(
    generated_files_path: str,
    components: Set[ParserComponents],
    gpu_location: GpuLocation,
    interactive: bool = False,
) -> list:
    generated_files_path = generated_files_path.rstrip("/")

    def read_file(name: str) -> str:
        path = os.path.join(generated_files_path, name)
        try:
            with open(path, "r") as f:
                output = f.read()
            return output
        except FileNotFoundError:
            raise InputFileNotFoundError(path)

    result = []

    # TODO: if linux, else windows
    if sys.platform == "win32":
        pass
    else:
        if not components.isdisjoint({ParserComponents.CASE, ParserComponents.MOTHERBOARD}):
            result += parse_motherboard(
                read_file("baseboard.txt"),
                read_file("connector.txt"),
                read_file("net.txt"),
                interactive,
            )
            if gpu_location == GpuLocation.MOTHERBOARD:
                _merge_gpu(
                    result,
                    "motherboard",
                    parse_lspci_and_glxinfo(False, read_file("lspci.txt"), ""),
                )
        if ParserComponents.CASE in components:
            result += parse_case(read_file("chassis.txt"), _find_component("motherboard", result))
        if ParserComponents.CPU in components:
            result += parse_lscpu(read_file("lscpu.txt"))
            if gpu_location == GpuLocation.CPU:
                _merge_gpu(
                    result,
                    "cpu",
                    parse_lspci_and_glxinfo(False, read_file("lspci.txt"), ""),
                )
        if ParserComponents.GPU in components and gpu_location == GpuLocation.DISCRETE:
            result += parse_lspci_and_glxinfo(True, read_file("lspci.txt"), read_file("glxinfo.txt"), interactive)
        if ParserComponents.RAM in components:
            ram_result = parse_decode_dimms(read_file("dimms.txt"), interactive)
            tmp: list[dict] = ram_result.copy()
            for item in tmp:
                item.pop("ram-ecc", None)
                item.pop("ram-timings", None)

            for bank in parse_udevadm(read_file("udevadm.txt")):
                for item in tmp:
                    if item["sn"] == bank["sn"]:
                        if any([item[k] != bank[k] for k in item]):  # they found the same item but they are different, manual review is needed
                            ram_result.append(bank)
                            tmp.append(bank)
                        break
                else:  # no break, udevadm found an item that decode-dimms missed
                    tmp.append(bank)
                    ram_result.append(bank)

            result += ram_result
        if ParserComponents.HDD in components or ParserComponents.SSD in components:
            result += parse_smartctl(read_file("smartctl.txt"), interactive)
        if ParserComponents.PSU in components:
            result += parse_psu(_find_component("case", result))

    result = _do_cleanup(result, interactive)
    return result


def split_products(parsed: List[dict]) -> List[dict]:
    item_keys = item_only_features()
    bmv = [
        "brand",
        "model",
        "variant",
    ]
    both = [
        "type",
    ]

    final_result = []
    products = []

    for item in parsed:
        if can_be_product(item):
            if item.get("variant", "") == "":
                item["variant"] = "default"
            new_product = {k: item.get(k) for k in bmv if k in item.keys()}
            found = False
            for old_product in products:
                if new_product.items() <= old_product.items():
                    found = True
                    break
            if not found:
                new_product.update(
                    {
                        "type": "P",
                        "features": {k: v for k, v in item.items() if k not in bmv + item_keys},
                    }
                )
                products.append(new_product)
        new_item = {
            "type": "I",
            "features": {k: v for k, v in item.items() if k in bmv + both + item_keys},
            "contents": [],
        }
        final_result.append(new_item)

    final_result += products
    return final_result


def item_only_features():
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
    return item_keys


def add_owner(parsed_items_only: List[dict], owner: str) -> List[dict]:
    for item in parsed_items_only:
        item["owner"] = owner
    return parsed_items_only


def add_chassis_code(parsed: List[dict], code: str) -> bool:
    for item in parsed:
        if item.get("type") == "I":
            if item.get("features", {}).get("type") == "case":
                item["code"] = code
                return True
    return False


def can_be_product(component: dict):
    # check if brand and model exist
    if "brand" not in component or "model" not in component:
        return False

    return True


def _do_cleanup(result: List[dict], verbose: bool = False) -> List[dict]:
    by_type = {}

    for item in result:
        removed = set()
        for k, v in item.items():
            # Check for k in these?
            # "brand",
            # "brand-manufacturer",
            # "model",
            # "integrated-graphics-brand",
            # "integrated-graphics-model",
            if isinstance(v, str) and v.lower() in MEANINGLESS_VALUES:
                removed.add(k)
            elif v is None:
                removed.add(k)
        for removed_thing in removed:
            del item[removed_thing]
        the_type = item.get("type")
        if the_type not in by_type:
            by_type[the_type] = []
        by_type[the_type].append(item)

        if verbose and len(removed) > 0:
            print(f"WARNING: Removed from {item.get('type', 'item with no type')}: {', '.join(removed)}.")

    for case in by_type.get("case", []):
        for mobo in by_type.get("motherboard", []):
            try:
                if (case["model"], case["brand"], case["variant"]) == (
                    mobo["brand"],
                    mobo["model"],
                    mobo["variant"],
                ):
                    case.pop("model")
            except KeyError:
                pass

    # avoid bad associations between items and products
    if len(result) > 1:
        for component1 in result:
            i = 1
            for component2 in result[i:]:
                if component1["type"] != component2["type"]:
                    if can_be_product(component1) and can_be_product(component2):
                        if (component1["brand"], component2["model"]) == (
                            component2["brand"],
                            component2["model"],
                        ):
                            variant1 = component1.get("variant", "")
                            variant2 = component2.get("variant", "")
                            if variant1 == variant2:
                                component1["variant"] = variant1.rstrip().join(f"_{component1['type']}").lstrip("_")
                                component2["variant"] = variant2.rstrip().join(f"_{component2['type']}").lstrip("_")

    return result


def _should_be_in_motherboard(the_type: str, features: dict) -> bool:
    if the_type in ("cpu", "ram"):
        return True
    if the_type.endswith("-card"):
        return True
    if the_type == "ssd":
        if features.get("hdd-form-factor", None) in ("m2", "m2.2"):
            return True
    return False


def _should_be_in_case(the_type: str, features: dict) -> bool:
    if the_type in ("motherboard", "hdd", "ssd", "odd", "fdd", "psu"):
        return True
    # Fallback for when there's no motherboard
    return _should_be_in_motherboard(the_type, features)


def unmake_tree(items_and_products: List[dict]) -> List[dict]:
    result = []

    for thing in items_and_products:
        result.append(thing)
        if thing.get("type") == "I":
            if "contents" in thing:
                result += unmake_tree(thing["contents"])
                thing["contents"] = []
    return result


def make_tree(items_and_products: List[dict]) -> List[dict]:
    items_and_products = copy.deepcopy(items_and_products)
    by_type = {}
    products = []

    for thing in items_and_products:
        if thing.get("type") == "I":
            if "features" in thing:
                the_type = thing["features"].get("type")
                if the_type not in by_type:
                    by_type[the_type] = []
                by_type[the_type].append(thing)
                continue

        products.append(thing)

    if "motherboard" in by_type:
        containers = by_type["motherboard"]
        del by_type["motherboard"]
        for the_type in by_type:
            save = []
            for thing in by_type[the_type]:
                if _should_be_in_motherboard(the_type, thing.get("features", {})):
                    if "contents" not in containers[0]:
                        containers[0]["contents"] = []
                    containers[0]["contents"].append(thing)
                else:
                    save.append(thing)
            by_type[the_type] = save
        save2 = {}
        for the_type in by_type:
            if len(by_type[the_type]) > 0:
                save2[the_type] = by_type[the_type]
        by_type = save2
        by_type["motherboard"] = containers

    if "case" in by_type:
        containers = by_type["case"]
        del by_type["case"]
        for the_type in by_type:
            save = []
            for thing in by_type[the_type]:
                if _should_be_in_case(the_type, thing.get("features", {})):
                    if "contents" not in containers[0]:
                        containers[0]["contents"] = []
                    containers[0]["contents"].append(thing)
                else:
                    save.append(thing)
                by_type[the_type] = save
        save2 = {}
        for the_type in by_type:
            if len(by_type[the_type]) > 0:
                save2[the_type] = by_type[the_type]
        by_type = save2
        by_type["case"] = containers

    top_items = []
    for the_type in by_type:
        top_items += by_type[the_type]

    return top_items + products


def check_required_files(path, is_gui: bool = False):
    if os.path.isdir(path):
        files_in_dir = os.listdir(path)
        if not files_in_dir:
            return ""
        for file in required_files():
            for file_in_dir in files_in_dir:
                if file_in_dir == file:
                    break
            else:
                if is_gui:
                    error = f"Missing file {file}\n"
                    return error
                else:
                    print(f"[bold red]Missing file {file}\n" f"Please re-run this script without the -f or --files option.[/]")
                    exit(1)
    return ""


def env_to_bool(value: Optional[str]) -> bool:
    try:
        if value.lower() in ("1", "true", "t", "", "yes", "y"):
            return True
    except AttributeError:
        pass

    return False
