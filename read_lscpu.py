#!/usr/bin/env python3

import sys

"""
Read "lscpu" output
"""


class CPU:
    def __init__(self):
        self.type = "cpu"
        self.architecture = ""
        self.model = ""
        self.brand = ""
        self.n_cores = -1  # core-n on TARALLO
        self.n_threads = -1  # thread-n on TARALLO
        self.frequency = -1
        self.human_readable_frequency = "N/A"  # TODO: calculate it or remove it


def read_lscpu(path: str):
    # print("Reading lscpu...")

    cpu = CPU()

    output = get_output(path)

    for line in output.splitlines():
        if "Architecture" in line:
            cpu.architecture = line.split("Architecture:")[1].strip()

        elif "Model name" in line:
            tmp = line.split("Model name:")[1].split("@")
            cpu.model = tmp[0].strip()

        elif "Vendor ID" in line:
            cpu.brand = line.split("Vendor ID:")[1].strip()

        elif "CPU max MHz" in line:
            # It's formatted with "%.4f" by lscpu, at the moment
            # https://github.com/karelzak/util-linux/blob/master/sys-utils/lscpu.c#L1246
            # .replace() needed because "ValueError: could not convert string to float: '3300,0000'"
            frequency_mhz = float(line.split("CPU max MHz:")[1].strip().replace(',', '.'))
            cpu.frequency = int(frequency_mhz * 1000 * 1000)

        elif "Thread(s) per core" in line:
            cpu.n_threads = int(line.split("Thread(s) per core:")[1].strip())

        elif "Core(s) per socket:" in line:
            cpu.n_cores = int(line.split("Core(s) per socket:")[1].strip())
            if cpu.n_threads != -1:
                cpu.n_threads *= cpu.n_cores

    return {
        "type": "cpu",
        "architecture": cpu.architecture,
        "model": cpu.model,
        "brand": cpu.brand,
        "core-n": cpu.n_cores,
        "thread-n": cpu.n_threads,
        "frequency-hertz": cpu.frequency,
        "human_readable_frequency": cpu.human_readable_frequency
    }


def get_output(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("Cannot open file.")
        print("Make sure to execute 'sudo ./generate_files.sh' first!")
        exit(-1)


if __name__ == '__main__':
    print(read_lscpu(sys.argv[1]))
