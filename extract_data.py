#!/bin/usr/python3

"""
Collect data from all the 'read...' scripts and returns it as a list of dicts
"""

from read_decode_dimms import read_decode_dimms
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
# TODO: add remaining files


def extract_and_collect_data_from_generated_files(has_dedicated_gpu: bool):
    return [].extend(read_lspci_and_glxinfo(has_dedicated_gpu, "tmp/lspci.txt", "tmp/glxinfo.txt"))\
        .extend(read_decode_dimms("tmp/dimms.txt"))

if __name__ == '__main__':
    extract_and_collect_data_from_generated_files()