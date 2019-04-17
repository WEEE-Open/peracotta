#!/usr/bin/env python3

"""
Read "lspci -v" output
"""

# TODO: add specs from lvps's messages - everything is a single function which gets called
class VideoCard:
    def __init__(self):
        self.type = "graphics-card"
        self.brand = ""
        self.model = ""
        self.vram_capacity = -1 # bytes

# ASK THE USER
has_dedicated = None
integrated_in_mobo = None
while True:
    dedicated = input("Does this system have a dedicated video card? Y/N:\n")
    if dedicated.lower() == "y":
        has_dedicated = True
        break
    elif dedicated.lower() == "n":
        has_dedicated = False
        while True:
            where_is_integrated = input("Is the video card integrated in the motherboard (press M)"
                                       " or in the CPU (press C)? Tip: the older the system,"
                                       " the higher the chance the GPU is integrated in the"
                                       " motherboard.\n")
            if where_is_integrated.lower() == "m":
                integrated_in_mobo = True
                break
            elif where_is_integrated.lower() == "c":
                integrated_in_mobo = False
                break
            else:
                print("Please enter 'M' for motherboard or 'C' for CPU.")
                continue
        break
    else:
        print("Please enter 'Y' or 'N'")
        continue

gpu = VideoCard()

"""START TEST"""
glxinfo_path = ""
lspci_path = ""

# dedicated
_2018mbp = 0
_2014mbp = 0
castes_pc = 0
_9400gt = 0
gtx970 = 1

# integrated
# jm11 = 0
_8300gt = 0
_82865g = 0
es1000 = 0

if _2018mbp:
    glxinfo_path = "2018-castes-mbp/glxinfo.txt"
    lspci_path = "2018-castes-mbp/lspci.txt"
elif _2014mbp:
    glxinfo_path = "2014-castes-mbp/glxinfo.txt"
    lspci_path = "2014-castes-mbp/lspci.txt"
elif castes_pc:
    glxinfo_path = "castes-pc/glxinfo.txt"
    lspci_path = "castes-pc/lspci.txt"
elif _9400gt:
    glxinfo_path = "glxinfo+lspci/dedicated/glxinfo-9400GT.txt"
    lspci_path = "glxinfo+lspci/dedicated/lspci-9400GT.txt"
elif gtx970:
    glxinfo_path = "glxinfo+lspci/dedicated/glxinfo-gtx-970.txt"
    lspci_path = "glxinfo+lspci/dedicated/lspci-gtx-970.txt"
# elif jm11:
#     glxinfo_path = "castes-pc/glxinfo.txt"
#     lspci_path = "castes-pc/lspci.txt"
elif _8300gt:
    glxinfo_path = "glxinfo+lspci/integrated/on-mobo/glxinfo-8300GT.txt"
    lspci_path = "glxinfo+lspci/integrated/on-mobo/lspci-8300GT.txt"
elif _82865g:
    glxinfo_path = "glxinfo+lspci/integrated/on-mobo/glxinfo-82865G.txt"
    lspci_path = "glxinfo+lspci/integrated/on-mobo/lspci-82865G.txt"
elif castes_pc:
    glxinfo_path = "glxinfo+lspci/integrated/on-mobo/glxinfo-ES1000.txt"
    lspci_path = "glxinfo+lspci/integrated/on-mobo/lspci-ES1000.txt"
"""END TEST"""

# SCRIPT
if has_dedicated:
    try:
        with open("tests/" + lspci_path, 'r') as f:
            print("Reading lspci -v...")
            lspci_output = f.read()
        with open("tests/" + glxinfo_path, 'r') as f:
            print("Reading glxinfo...")
            glxinfo_output = f.read()
    except FileNotFoundError:
        print("Cannot open file.")
        print("Make sure to execute 'sudo ./generate_files.sh' first!")
        exit(-1)

    lspci_sections = lspci_output.split("\n\n")

    for section in lspci_sections:
        if "VGA compatible controller" in section:
            first_line = section.splitlines()[0]
            # take the first string between [] from the first line
            gpu.model = first_line.split("[")[1].split("]")[0]

            if "AMD" in gpu.model or "ATI" in gpu.model:
                gpu.brand = gpu.model
                # take second string between []
                gpu.model = first_line.split("[")[2].split("]")[0]
            else:
                if "NVIDIA" in first_line.upper():
                    gpu.brand = "NVIDIA"
                else:
                    while True:
                        tmp = input("I couldn't find the Video Card brand. Please enter it below:\n")
                        confirm = input("Confirm " + str(tmp) + " as the Video Card brand? Y/N\n")
                        if confirm.lower() == "y":
                            gpu.brand = tmp
                            print("GPU brand confirmed, continuing...")
                            break
                        else:
                            print("Please enter the brand/manufacturer again:")
                            continue

    for line in glxinfo_output.splitlines():
        if "Dedicated video memory" in line:
            try:
                tmp_vram = int(line.split(" ")[7].split(" ")[0])
                tmp_vram_multiplier = line[-2:]
            except ValueError as ve:
                print("There was a problem reading glxinfo's output. Please try again or run generate_files.sh again.")
                print(ve)
                exit(-1)

            gpu.vram_capacity = tmp_vram

            if tmp_vram_multiplier == "GB":
                gpu.vram_capacity *= 1024*1024*1024
            elif tmp_vram_multiplier == "MB":
                gpu.vram_capacity *= 1024*1024
            elif tmp_vram_multiplier.upper() == "KB":
                gpu.vram_capacity *= 1024
            else:
                print("The VRAM capacity could not be detected. Please try looking for it on the Video Card or on the Internet.")
                # gpu.vram_capacity = -1

            # for line in section.splitlines():
                # # only considering prefetchable VRAM
                # # TODO: delete code below, prefetchable does not mean VRAM
                # if "Memory" in line and "non" not in line and "prefetchable" in line:
                #     vram = line.split("size=")[1].split("]")[0]
                #     last_char = vram[-1].upper()
                #     size = int(vram[:-1])
                #
                #     # selects biggest prefetchable memory
                #     if gpu.vram_capacity < size:
                #         gpu.vram_capacity = size
                #     else:
                #         break
                #
                #     if last_char == "M":
                #         gpu.vram_capacity_multiplier = "M"
                #     elif last_char == "K":
                #         gpu.vram_capacity_multiplier = "K"
                #     elif last_char == "G":
                #         gpu.vram_capacity_multiplier = "G"
                #     else:
                #         while True:
                #             tmp = input("I couldn't find the VRAM Capacity. Please check the VRAM (Video Memory) of the card"
                #                         " and enter it below: \nformat: <integer><K/M/G for Kilobytes/Megabytes/Gigabytes\n"
                #                         "e.g. 256M\n")
                #             multiplier = tmp[-1].upper()
                #             mult_full = ""
                #             if multiplier == "K":
                #                 mult_full = "Kilobytes"
                #             elif multiplier == "M":
                #                 mult_full = "Megabytes"
                #             elif multiplier == "G":
                #                 mult_full = "Gigabytes"
                #             else:
                #                 print("Unrecognized format. Please try again.")
                #                 continue
                #
                #             try:
                #                 size = int(tmp[:-1])
                #             except ValueError:
                #                 print("Unrecognized format. Please try again.")
                #                 continue
                #
                #             confirm = input("Confirm the VRAM has a capacity of " + str(size) + " " + mult_full + " Y/N\n")
                #             if confirm.lower() == "y":
                #                 gpu.vram_capacity = size
                #                 gpu.vram_capacity_multiplier = multiplier
                #                 break
                #             else:
                #                 print("Enter a new value.")
                #                 continue

            # break


else:
    if integrated_in_mobo:
        pass
    else: # integrated_in_cpu
        pass
        # TODO: write code

print(gpu.brand)
print(gpu.model)
print(str(gpu.vram_capacity))

# if name == __main__:
#     read_lspci_-v_and_glxinfo()