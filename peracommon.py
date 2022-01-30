#!/usr/bin/env python3
import os
import subprocess


def check_dependencies_for_generate_files():
    exit_value = os.system(
        "dpkg -s pciutils i2c-tools mesa-utils smartmontools dmidecode > /dev/null"
    )
    return exit_value == 0


def generate_files(path: str):
    os.makedirs(path, exist_ok=True)

    subprocess.run(["../scripts/generate_files.sh", path])
