#!/usr/bin/env python3

"""
Read "lspci -v" and "glxinfo" outputs
"""

import re

class VideoCard:
    def __init__(self):
        self.type = "graphics-card"
        self.manufacturer_brand = ""
        self.reseller_brand = ""
        self.model = ""
        self.capacity = -1 # bytes
        self.human_readable_capacity = ""

def parse_lspci_output(gpu:VideoCard, lspci_path:str):
    try:
        # TODO: reformat path for general use - also best to assume working directory
        with open("tests/" + lspci_path, 'r') as f:
            print("Reading lspci -v...")
            lspci_output = f.read()
    except FileNotFoundError:
        print("Cannot open file.")
        print("Make sure to execute 'sudo ./generate_files.sh' first!")
        exit(-1)

    lspci_sections = lspci_output.split("\n\n")

    for section in lspci_sections:
        if "VGA compatible controller" in section:
            first_line = section.splitlines()[0]
            second_line = section.splitlines()[1]
            try:
                # take the first string between [] from the first line
                # works with NVIDIA cards
                gpu.model = first_line.split("[")[1].split("]")[0]
            except Exception:
                # there may not be an argument in between []
                pass

            if "AMD" in gpu.model or "ATI" in gpu.model:
                gpu.manufacturer_brand = gpu.model
                # take second string between []
                gpu.model = first_line.split("[")[2].split("]")[0]
                if "controller" in gpu.model:
                    gpu.model = section.splitlines()[1].split(" ")[-1]
            else:
                if "NVIDIA" in first_line.upper():
                    gpu.manufacturer_brand = "NVIDIA"

                elif "Intel" in first_line:
                    gpu.manufacturer_brand = "Intel"
                    if "Integrated Graphics" in first_line:
                        tmp_model = first_line.split("Intel Corporation ")[1].split(" Integrated Graphics")[0]
                        # if there are no numbers, e.g. "Core Processor", tmp_model is not a model number
                        if not re.search('\d+', tmp_model):
                            tmp_model = ""
                    elif "[" in first_line and "]" in first_line:
                        tmp_model = first_line.split("[")[1].split("]")[0]
                    else:
                        tmp_model = ""

                    if tmp_model != "":
                        gpu.model = tmp_model
                    else:
                        gpu.model = None
                        print("I couldn't find the Integrated Graphics model. "
                              "The model was set to 'None' and is to be edited logging into the TARALLO afterwards. "
                              "The information you're looking for should be in the following 2 lines:\n"
                              + first_line + "\n"
                              + second_line + "\n")

                else:
                    gpu.manufacturer_brand = None
                    print("I couldn't find the Video Card brand. "
                          "The model was set to 'None' and is to be edited logging into the TARALLO afterwards. "
                          "The information you're looking for should be in the following 2 lines:\n"
                          + first_line + "\n"
                          + second_line + "\n")
            break



def parse_glxinfo_output(gpu:VideoCard, glxinfo_path:str):
    try:
        # TODO: reformat path for general use
        with open("tests/" + glxinfo_path, 'r') as f:
            print("Reading glxinfo...")
            glxinfo_output = f.read()
    except FileNotFoundError:
        print("Cannot open file.")
        print("Make sure to execute 'sudo ./generate_files.sh' first!")
        exit(-1)

    glxinfo_output_len = len(glxinfo_output.splitlines())

    for i, line in enumerate(glxinfo_output.splitlines()):
        dedicated_memory_found = False

        # this line comes before the "Dedicated video memory" line
        # this basically saves a default value if the dedicated memory line cannot be found
        if "Video memory" in line:
            try:
                tmp_vid_mem = int(line.split(" ")[6].split(" ")[0][:-2])
                tmp_vid_mem_multiplier = line[-2:]
            except ValueError:
                print("There was a problem reading glxinfo's output. Please try again or run generate_files.sh again.")
                exit(-1)

            gpu.capacity = tmp_vid_mem

            if tmp_vid_mem_multiplier == "GB":
                gpu.human_readable_capacity = str(tmp_vid_mem) + " " + tmp_vram_multiplier
                gpu.capacity *= 1024 * 1024 * 1024
            elif tmp_vid_mem_multiplier == "MB":
                gpu.human_readable_capacity = str(tmp_vid_mem) + " " + tmp_vram_multiplier
                gpu.capacity *= 1024 * 1024
            elif tmp_vid_mem_multiplier.upper() == "KB":
                gpu.human_readable_capacity = str(tmp_vid_mem) + " " + tmp_vram_multiplier
                gpu.capacity *= 1024
            else:
                gpu.capacity = -1
                print("The VRAM capacity could not be detected. "
                      "Please try looking for it on the Video Card or on the Internet. "
                      "The detected value defaulted to -1.")

        if "Dedicated video memory" in line:

            dedicated_memory_found = True

            try:
                tmp_vram = int(line.split(" ")[7].split(" ")[0])
                tmp_vram_multiplier = line[-2:]
            except ValueError:
                print("There was a problem reading glxinfo's output. Please try again or run generate_files.sh again.")
                exit(-1)

            gpu.capacity = tmp_vram

            if tmp_vram_multiplier == "GB":
                gpu.human_readable_capacity = str(tmp_vram) + " " + tmp_vram_multiplier
                gpu.capacity *= 1024 * 1024 * 1024
                break
            elif tmp_vram_multiplier == "MB":
                gpu.human_readable_capacity = str(tmp_vram) + " " + tmp_vram_multiplier
                gpu.capacity *= 1024 * 1024
                break
            elif tmp_vram_multiplier.upper() == "KB":
                gpu.human_readable_capacity = str(tmp_vram) + " " + tmp_vram_multiplier
                gpu.capacity *= 1024
                break
            else:
                print("The dedicated video memory could not be found. "
                      "A video memory value will try to be found, which needs to be corrected by hand. "
                      "Ugh, humans.")

        if i == glxinfo_output_len - 1 and not dedicated_memory_found:
            if gpu.capacity == -1:
                print("A dedicated video memory couldn't be found. "
                      "Value defaulted to -1. "
                      "Please humans, fix this error by hand.")
            else:
                print("A dedicated video memory couldn't be found. "
                      "A generic video memory capacity was found instead, which could be near the actual value. "
                      "Please humans, fix this error by hand.")

# SCRIPT
def read_lspci_and_glxinfo(has_dedicated:bool, lspci_path:str, glxinfo_path:str):
    gpu = VideoCard()
    if has_dedicated:
        parse_lspci_output(gpu, lspci_path)
        parse_glxinfo_output(gpu, glxinfo_path)
    else: # integrated_in_mobo or integrated_in_cpu
        parse_lspci_output(gpu, lspci_path)
        # don't parse glxinfo because the VRAM is part of the RAM and varies
        gpu.capacity = None
        print("The VRAM capacity could not be detected. "
              "Please try looking for it on the Video Card or on the Internet. "
              "The capacity value defaulted to 'None'. "
              "For an integrated GPU, the VRAM may also be shared with the system RAM, so an empty value is acceptable.")

    # TODO: comment following lines in production code
    print(gpu.manufacturer_brand)
    print(gpu.model)
    print(str(gpu.capacity))
    print(gpu.human_readable_capacity)

    return {
        "type": "graphics-card",
        "manufacturer_brand": gpu.manufacturer_brand,
        "reseller_brand": gpu.reseller_brand,
        "model": gpu.model,
        "capacity": gpu.capacity,
        "human_readable_capcity": gpu.human_readable_capacity
    }

if __name__ == '__main__':
    read_lspci_and_glxinfo()