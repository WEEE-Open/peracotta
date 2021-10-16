#!/usr/bin/env python3

import sys
from dataclasses import dataclass

from InputFileNotFoundError import InputFileNotFoundError

"""
Read "lscpu" output
"""


@dataclass
class CPU:
    type = "cpu"
    architecture = ""
    model = ""
    brand = ""
    n_cores = -1  # core-n on TARALLO
    n_threads = -1  # thread-n on TARALLO
    frequency = -1


def read_lscpu(path: str):
    cpu = CPU()

    output = get_output(path)
    tmp_freq = None
    sockets = 1

    for line in output.splitlines():
        if "Architecture:" in line:
            architecture = line.split("Architecture:")[1].strip()
            if architecture == "x86_64":
                cpu.architecture = "x86-64"
            if architecture in ("i686", "i586", "i486", "i386"):
                cpu.architecture = "x86-32"
        elif "CPU op-mode(s):" in line:
            architecture = line.split("CPU op-mode(s):")[1].strip()
            if cpu.architecture.startswith("x86"):
                if "64-bit" in architecture:
                    cpu.architecture = "x86-64"
        elif "Model name:" in line:
            tmp = line.split("Model name:")[1].rsplit("@", 1)
            cpu.model = tmp[0].strip()
            if "@" in line:
                tmp_freq = tmp[1].replace("GHz", "").strip()
            elif line.endswith("GHz"):
                tmp_freq = line.rsplit(" ", 1)[1][:-3]

            if cpu.model.startswith("Intel"):
                # To remove "(R)", or don't if it's not there
                cpu.model = cpu.model.split(" ", 1)[1]
            if cpu.model.endswith("-Core Processor"):
                cpu.model = cpu.model.rsplit(" ", 2)[0]

            # Remove some more lapalissades and assorted tautologies
            cpu.model = (
                cpu.model.replace("(R)", " ")
                .replace("(TM)", " ")
                .replace("(tm)", " ")
                .replace("CPU", "")
                .replace("AMD", " ")
                .replace("Dual-Core", "")
                .replace("Quad-Core", "")
                .replace("Octa-Core", "")
                .replace("Processor", "")
                .replace("processor", "")
                .strip()
            )

            while "  " in cpu.model:
                cpu.model = cpu.model.replace("  ", " ")

        elif "Vendor ID:" in line:
            cpu.brand = line.split("Vendor ID:")[1].strip()
            if cpu.brand == "GenuineIntel":
                cpu.brand = "Intel"
            elif cpu.brand == "AuthenticAMD":
                cpu.brand = "AMD"

        elif "CPU max MHz:" in line:
            # It's formatted with "%.4f" by lscpu, at the moment
            # https://github.com/karelzak/util-linux/blob/master/sys-utils/lscpu.c#L1246
            # .replace() needed because "ValueError: could not convert string to float: '3300,0000'"
            frequency_mhz = float(
                line.split("CPU max MHz:")[1].strip().replace(",", ".")
            )
            cpu.frequency = int(frequency_mhz * 1000 * 1000)

        elif "Thread(s) per core:" in line:
            cpu.n_threads = int(line.split("Thread(s) per core:")[1].strip())

        elif "Core(s) per socket:" in line:
            cpu.n_cores = int(line.split("Core(s) per socket:")[1].strip())
            if cpu.n_threads != -1:
                cpu.n_threads *= cpu.n_cores

        elif "Socket(s):" in line:
            sockets = int(line.split("Socket(s):")[1].strip())

    if tmp_freq is not None:
        cpu.frequency = int(float(tmp_freq.replace(",", ".")) * 1000 * 1000 * 1000)

    result = {
        "type": "cpu",
        "working": "yes",  # Indeed it is working
        "isa": cpu.architecture,
        "model": cpu.model,
        "brand": cpu.brand,
        "core-n": cpu.n_cores,
        "thread-n": cpu.n_threads,
        "frequency-hertz": cpu.frequency,
    }

    if sockets > 1:
        result = [result] * sockets

    return result


def get_output(path):
    try:
        with open(path, "r") as f:
            output = f.read()
    except FileNotFoundError:
        raise InputFileNotFoundError(path)
    return output


if __name__ == "__main__":
    import json

    try:
        print(json.dumps(read_lscpu(sys.argv[1]), indent=2))
    except InputFileNotFoundError as e:
        print(str(e))
        exit(1)
