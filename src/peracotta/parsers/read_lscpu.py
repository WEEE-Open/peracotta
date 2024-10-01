#!/usr/bin/env python3


"""
Read "lscpu" output
"""
from typing import List


def parse_lscpu(lscpu: str) -> List[dict]:
    cpu = {
        "type": "cpu",
        "working": "yes",
    }

    tmp_freq = None
    sockets = 1

    for line in lscpu.splitlines():
        if "Architecture:" in line:
            architecture = line.split("Architecture:")[1].strip()
            if architecture == "x86_64":
                cpu["isa"] = "x86-64"
            if architecture in ("i686", "i586", "i486", "i386"):
                cpu["isa"] = "x86-32"
        elif "CPU op-mode(s):" in line:
            architecture = line.split("CPU op-mode(s):")[1].strip()
            if cpu["isa"].startswith("x86"):
                if "64-bit" in architecture:
                    cpu["isa"] = "x86-64"
        elif "Model name:" in line:
            tmp = line.split("Model name:")[1].rsplit("@", 1)
            cpu["model"] = tmp[0].strip()
            if "@" in line:
                tmp_freq = tmp[1].replace("GHz", "").strip()
            elif line.endswith("GHz"):
                tmp_freq = line.rsplit(" ", 1)[1][:-3]

            if cpu["model"].startswith("Intel"):
                # To remove "(R)", or don't if it's not there
                cpu["model"] = cpu["model"].split(" ", 1)[1]
            if cpu["model"].endswith("-Core Processor"):
                cpu["model"] = cpu["model"].rsplit(" ", 2)[0]

            # Remove some more lapalissades and assorted tautologies
            cpu["model"] = (
                cpu["model"]
                .replace("(R)", " ")
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

            while "  " in cpu["model"]:
                cpu["model"] = cpu["model"].replace("  ", " ")

        elif "Vendor ID:" in line:
            cpu["brand"] = line.split("Vendor ID:")[1].strip()
            if cpu["brand"] == "GenuineIntel":
                cpu["brand"] = "Intel"
            elif cpu["brand"] == "AuthenticAMD":
                cpu["brand"] = "AMD"

        elif "CPU max MHz:" in line:
            # It's formatted with "%.4f" by lscpu, at the moment
            # https://github.com/karelzak/util-linux/blob/master/sys-utils/lscpu.c#L1246
            # .replace() needed because "ValueError: could not convert string to float: '3300,0000'"
            frequency_mhz = float(line.split("CPU max MHz:")[1].strip().replace(",", "."))
            cpu["frequency-hertz"] = int(frequency_mhz * 1000 * 1000)

        elif "CPU MHz:" in line and "frequency-hertz" not in cpu:
            # This may not exist anymore (?) but we should use it as a fallback
            frequency_mhz = float(line.split("CPU MHz:")[1].strip().replace(",", "."))
            cpu["frequency-hertz"] = int(frequency_mhz * 1000 * 1000)

        elif "Thread(s) per core:" in line:
            cpu["thread-n"] = int(line.split("Thread(s) per core:")[1].strip())

        elif "Core(s) per socket:" in line:
            cpu["core-n"] = int(line.split("Core(s) per socket:")[1].strip())
            if "thread-n" in cpu:
                cpu["thread-n"] *= cpu["core-n"]

        elif "Socket(s):" in line:
            sockets = int(line.split("Socket(s):")[1].strip())

    if tmp_freq is not None:
        cpu["frequency-hertz"] = int(float(tmp_freq.replace(",", ".")) * 1000 * 1000 * 1000)

    cpu = [cpu]
    if sockets > 1:
        cpu = cpu * sockets

    return cpu


if __name__ == "__main__":
    import json
    import sys

    try:
        with open(sys.argv[1], "r") as f:
            input_file = f.read()
        print(json.dumps(parse_lscpu(input_file), indent=2))
    except BaseException as e:
        print(str(e))
        exit(1)
