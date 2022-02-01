#!/usr/bin/env python3
import os
import subprocess
import sys
from enum import Enum

from parsers.read_decode_dimms import parse_decode_dimms
from parsers.read_dmidecode import parse_motherboard
from parsers.read_lscpu import parse_lscpu
from parsers.read_lspci_and_glxinfo import parse_lspci_and_glxinfo


class InputFileNotFoundError(FileNotFoundError):
    def __init__(self, path):
        super().__init__(f"Cannot open file {path}")
        self.path = path

    def get_path(self):
        return self.path


@Enum.unique
class GpuLocation(Enum):
    NONE = 0
    DISCRETE = 1
    CPU = 2
    MOTHERBOARD = 3


def check_dependencies_for_generate_files():
    retval = os.system("dpkg -s pciutils i2c-tools mesa-utils smartmontools dmidecode > /dev/null")
    return retval == 0


def generate_files(path: str):
    os.makedirs(path, exist_ok=True)

    subprocess.run(["../scripts/generate_files.sh", path])


def _merge_gpu(current_results: list, target_type: str, gpus: list) -> None:
    # TODO: do this
    pass


def call_parsers(generated_files_path: str, components: set, gpu_location: GpuLocation) -> list:
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
        if not components.isdisjoint({"case", "motherboard"}):
            result += parse_motherboard(read_file("baseboard.txt"), read_file("connectors.txt"), read_file("net.txt"))
            if gpu_location == GpuLocation.MOTHERBOARD:
                _merge_gpu(result, "motherboard", parse_lspci_and_glxinfo(False, read_file("lspci.txt"), ""))
        if "cpu" in components:
            result += parse_lscpu(read_file("lscpu.txt"))
            if gpu_location == GpuLocation.CPU:
                _merge_gpu(result, "cpu", parse_lspci_and_glxinfo(False, read_file("lspci.txt"), ""))
        if "gpu" in components and gpu_location == GpuLocation.DISCRETE:
            result += parse_lspci_and_glxinfo(True, read_file("lspci.txt"), read_file("glxinfo.txt"))
        if "ram" in components:
            result += parse_decode_dimms(read_file("dimms.txt"))
        if "hdd" in components:
            result += parse_smartctl(read_file("smartctl.txt"))

    return result
