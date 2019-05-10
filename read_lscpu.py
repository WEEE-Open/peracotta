#!/usr/bin/env python3

import sys

'''
Read "lscpu" output
'''

class CPU:
    def __init__(self):
        self.type = "cpu"
        self.architecture = ""
        self.model = ""
        self.brand = ""
        self.n_cores = -1 # core-n on TARALLO
        self.n_threads = -1 # thread-n on TARALLO
        self.frequency = -1
        self.human_readable_frequency = ""

def read_lscpu(path: str):
    # print("Reading lscpu...")

    cpu = CPU()

    try:
        with open(path, 'r') as f:
            output = f.read()
    except FileNotFoundError:
        print("Cannot open file.")
        print("Make sure to execute 'sudo ./generate_files.sh' first!")
        exit(-1)

    for line in output.splitlines():
        if "Architecture" in line:
            cpu.architecture = line.split("Architecture:")[1].strip()

        elif "Model name" in line:
            tmp = line.split("Model name:")[1].split("@")
            cpu.model = tmp[0].strip()
            tmp_freq = tmp[1].strip()
            if tmp_freq is not None:
                if "GHz" in tmp_freq:
                    cpu.human_readable_frequency = tmp_freq
                    tmp_freq = float(tmp_freq[:-3])
                    cpu.frequency = tmp_freq * 1000 * 1000 * 1000

                elif "MHz" in tmp_freq:
                    cpu.human_readable_frequency = tmp_freq
                    tmp_freq = float(tmp_freq[:-3])
                    cpu.frequency = tmp_freq * 1000 * 1000

                elif "KHZ" in tmp_freq.upper():
                    cpu.human_readable_frequency = tmp_freq
                    tmp_freq = float(tmp_freq[:-3])
                    cpu.frequency = tmp_freq * 1000

        elif "Vendor ID" in line:
            cpu.brand = line.split("Vendor ID:")[1].strip()

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


if __name__ == '__main__':
    print(read_lscpu(sys.argv[1]))
