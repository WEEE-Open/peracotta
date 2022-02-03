#!/usr/bin/env python3
import os
import subprocess
import sys
from enum import Enum
from typing import Optional

from parsers.read_decode_dimms import parse_decode_dimms
from parsers.read_dmidecode import parse_motherboard, parse_case, parse_psu
from parsers.read_lscpu import parse_lscpu
from parsers.read_lspci_and_glxinfo import parse_lspci_and_glxinfo
from parsers.read_smartctl import parse_smartctl


class InputFileNotFoundError(FileNotFoundError):
    def __init__(self, path):
        super().__init__(f"Cannot open file {path}")
        self.path = path

    def get_path(self):
        return self.path


MEANINGLESS_VALUES = (
    "",
    "null",
    "custom",
    "unknown",
    "undefined",
    "no enclosure",
    "chassis manufacture",
    "to be filled by o.e.m",
    "to be filled by o.e.m.",
)


class GpuLocation(Enum):
    NONE = 0
    DISCRETE = 1
    CPU = 2
    MOTHERBOARD = 3


class ParserComponents(Enum):
    CASE = "case"
    MOTHERBOARD = "motherboard"
    CPU = "cpu"
    RAM = "ram"
    GPU = "gpu"
    HDD = "hdd"
    SSD = "ssd"

    @classmethod
    def all(cls):
        return list(cls)


def check_dependencies_for_generate_files():
    retval = os.system("dpkg -s pciutils i2c-tools mesa-utils smartmontools dmidecode > /dev/null")
    return retval == 0


def generate_files(path: str):
    os.makedirs(path, exist_ok=True)

    if os.geteuid() != 0:
        subprocess.run(["sudo", "scripts/generate_files.sh", path])
    else:
        subprocess.run(["scripts/generate_files.sh", path])


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


def _merge_gpu(current_results: list[dict], target_type: str, gpus: list) -> None:
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


def _find_component(component_type: str, result: list[dict]) -> Optional[dict]:
    for component in result:
        if "type" in component and component["type"] == component_type:
            return component
    return None


def _find_all_components(component_type: str, result: list[dict]) -> list[dict]:
    return_this = []
    for component in result:
        if "type" in component and component["type"] == component_type:
            return_this.append(component)
    return return_this


def call_parsers(generated_files_path: str, components: set[ParserComponents], gpu_location: GpuLocation) -> list:
    generated_files_path = generated_files_path.rstrip("/")

    def read_file(name: str) -> str:
        path = f"{generated_files_path}/{name}"
        try:
            with open(path, "r") as f:
                output = f.read()
            return output
        except FileNotFoundError:
            raise InputFileNotFoundError(path)

    result = []

    # TODO: if linux, else windows
    if sys.platform == 'win32':
        pass
    else:
        if not components.isdisjoint({ParserComponents.CASE, ParserComponents.MOTHERBOARD}):
            result += parse_motherboard(read_file("baseboard.txt"), read_file("connectors.txt"), read_file("net.txt"))
            if gpu_location == GpuLocation.MOTHERBOARD:
                _merge_gpu(result, "motherboard", parse_lspci_and_glxinfo(False, read_file("lspci.txt"), ""))

        if ParserComponents.CASE in components:
            result += parse_case(read_file("chassis.txt"), _find_component("motherboard", result))
        if ParserComponents.CPU in components:
            result += parse_lscpu(read_file("lscpu.txt"))
            if gpu_location == GpuLocation.CPU:
                _merge_gpu(result, "cpu", parse_lspci_and_glxinfo(False, read_file("lspci.txt"), ""))
        if ParserComponents.GPU in components and gpu_location == GpuLocation.DISCRETE:
            result += parse_lspci_and_glxinfo(True, read_file("lspci.txt"), read_file("glxinfo.txt"))
        if ParserComponents.RAM in components:
            result += parse_decode_dimms(read_file("dimms.txt"))
        if ParserComponents.HDD in components or ParserComponents.SSD in components:
            result += parse_smartctl(read_file("smartctl.txt"))
        if ParserComponents.PSU in components:
            result += parse_psu(_find_component("case", result))

    return result


def split_products(parsed: list[dict]) -> list[dict]:
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
    both = [
        "brand",
        "model",
        "variant",
        "type",
    ]

    final_result = []
    products = []

    for item in parsed:
        if can_be_product(item):
            if item.get("variant", "") == "":
                item["variant"] = "default"
            new_product = {
                k: item.get(k) for k in both if k in item.keys() and k != "type"
            }
            found = False
            for old_product in products:
                if new_product.items() <= old_product.items():
                    found = True
                    break
            if not found:
                new_product.update({
                    "type": "P",
                    "features": {k: v for k, v in item.items() if k not in item_keys},
                })
                products += new_product
        new_item = {
            "type": "I",
            "features": {k: v for k, v in item.items() if k in both + item_keys},
            "contents": [],
        }
        final_result += new_item

    return final_result


def add_owner(parsed: list[dict], owner: str) -> list[dict]:
    for item in parsed:
        item["owner"] = owner
    return parsed


def can_be_product(component: dict):
    # check if brand and model exist
    if "brand" not in component or "model" not in component:
        return False

    return True


def do_cleanup(result: list[dict], verbose: bool = False) -> None:
    by_type = {}
    removed = set()

    for item in result:
        for k, v in item.items():
            # Check for k in these?
            # "brand",
            # "brand-manufacturer",
            # "model",
            # "integrated-graphics-brand",
            # "integrated-graphics-model",
            if isinstance(v, str) and v.lower() in MEANINGLESS_VALUES:
                removed.add(k)
                del item[k]
            elif v is None:
                removed.add(k)
                del item[k]
        the_type = item.get("type")
        if the_type not in by_type:
            by_type[the_type] = []
        by_type[the_type].append(item)

        if verbose and len(removed) > 0:
            print(f"WARNING: Removed from {item['type']}: {', '.join(removed)}.")

    for case in by_type.get("case", []):
        for mobo in by_type.get("motherboard", []):
            try:
                if (case["model"], case["brand"], case["variant"]) ==\
                        (mobo["brand"], mobo["model"], mobo["variant"]):
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
                        if (component1["brand"], component2["model"]) ==\
                                (component2["brand"], component2["model"]):
                            variant1 = component1.get("variant", "")
                            variant2 = component2.get("variant", "")
                            if variant1 == variant2:
                                component1["variant"] = variant1.rstrip().join(f"_{component1['type']}").lstrip('_')
                                component2["variant"] = variant2.rstrip().join(f"_{component2['type']}").lstrip('_')


def _should_be_in_motherboard(the_type: str, features: dict) -> bool:
    if the_type in ("cpu", "ram"):
        return True
    if the_type.endswith('-card'):
        return True
    if the_type == 'ssd':
        if features.get("hdd-form-factor", None) in ("m2", "m2.2"):
            return True
    return False


def _should_be_in_case(the_type: str, features: dict) -> bool:
    if the_type in ("hdd", "ssd", "odd", "fdd", "psu"):
        return True
    # Fallback for when there's no motherboard
    return _should_be_in_motherboard(the_type, features)


def make_tree(items_and_products: list[dict]) -> list[dict]:
    by_type = {}
    result = []

    for thing in items_and_products:
        if thing.get("type") == 'I':
            if "features" in thing:
                if "type" in thing["features"]:
                    the_type = thing.get("type")
                    if the_type not in by_type:
                        by_type[the_type] = []
                    by_type[the_type].append(thing)
                    continue

        result.append(thing)

    if "motherboard" in by_type:
        containers = by_type["motherboard"]
        del by_type["motherboard"]
        for the_type in by_type:
            if _should_be_in_motherboard(the_type, by_type[the_type].get("features", {})):
                if "contents" not in containers[0]:
                    containers[0]["contents"] = []
                containers[0]["contents"] += by_type[the_type]
                del by_type[the_type]
        by_type["motherboard"] = containers

    if "case" in by_type:
        containers = by_type["case"]
        del by_type["case"]
        for the_type in by_type:
            if _should_be_in_motherboard(the_type, by_type[the_type].get("features", {})):
                if "contents" not in containers[0]:
                    containers[0]["contents"] = []
                containers[0]["contents"] += by_type[the_type]
                del by_type[the_type]
        by_type["case"] = containers

    top_items = []
    for the_type in by_type:
        for thing in by_type[the_type]:
            top_items += thing

    return top_items + result
