#!/usr/bin/env python3

"""
Read "lspci -v" and "glxinfo" outputs
"""

# TODO: add specs from @quel_tale's messages - everything is a single function which gets called
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

# dedicated:
_2018mbp = 0
_2014mbp = 0
castes_pc = 0
_9400gt = 0
gtx970 = 0
asdpc = 0
castes_HP_G100 = 0

# integrated:
# jm11 = 0
_8300gt = 0
_82865g =0
es1000 = 0
castes_HP_82945G = 0
acer_swift3 = 1
HP_elitebook_2540p = 1

# dedicated:
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
elif asdpc:
    glxinfo_path = "asdpc/glxinfo.txt"
    lspci_path = "asdpc/lspci.txt"
elif castes_HP_G100:
    glxinfo_path = "castes-HP-dc7600/NVIDIA-G100/glxinfo.txt"
    lspci_path = "castes-HP-dc7600/NVIDIA-G100/lspci.txt"

# integrated:
# elif jm11:
#     glxinfo_path = "castes-pc/glxinfo.txt"
#     lspci_path = "castes-pc/lspci.txt"
elif _8300gt:
    glxinfo_path = "glxinfo+lspci/integrated/on-mobo/glxinfo-8300GT.txt"
    lspci_path = "glxinfo+lspci/integrated/on-mobo/lspci-8300GT.txt"
elif _82865g:
    glxinfo_path = "glxinfo+lspci/integrated/on-mobo/glxinfo-82865G.txt"
    lspci_path = "glxinfo+lspci/integrated/on-mobo/lspci-82865G.txt"
elif es1000:
    glxinfo_path = "glxinfo+lspci/integrated/on-mobo/glxinfo-ES1000.txt"
    lspci_path = "glxinfo+lspci/integrated/on-mobo/lspci-ES1000.txt"
elif castes_HP_82945G:
    glxinfo_path = "castes-HP-dc7600/82945G/glxinfo.txt"
    lspci_path = "castes-HP-dc7600/82945G/lspci.txt"
elif acer_swift3:
    glxinfo_path = "glxinfo+lspci/integrated/on-cpu/Acer Swift 3/glxinfo.txt"
    lspci_path = "glxinfo+lspci/integrated/on-cpu/Acer Swift 3/lspci.txt"
elif HP_elitebook_2540p:
    glxinfo_path = "glxinfo+lspci/integrated/on-cpu/HP EliteBook 2540p (i5 M540)/glxinfo.txt"
    lspci_path = "glxinfo+lspci/integrated/on-cpu/HP EliteBook 2540p (i5 M540)/lspci.txt"
"""END TEST"""

def parse_lspci_output(lspci_path:str):
    try:
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
            try:
                # take the first string between [] from the first line
                # works with NVIDIA cards
                gpu.model = first_line.split("[")[1].split("]")[0]
            except Exception:
                # there may not be an argument in between []
                pass

            if "AMD" in gpu.model or "ATI" in gpu.model:
                gpu.brand = gpu.model
                # take second string between []
                gpu.model = first_line.split("[")[2].split("]")[0]
                if "controller" in gpu.model:
                    gpu.model = section.splitlines()[1].split(" ")[-1]
            else:
                if "NVIDIA" in first_line.upper():
                    gpu.brand = "NVIDIA"
                elif "Intel" in first_line:
                    gpu.brand = "Intel"
                    # TODO: check the following line is valid for other Intel integrated GPUs (works with 82865G)
                    gpu.model = first_line.split("Intel Corporation ")[1].split(" ")[0]
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



def parse_glxinfo_output(glxinfo_path:str):
    try:
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

            gpu.vram_capacity = tmp_vid_mem

            if tmp_vid_mem_multiplier == "GB":
                gpu.vram_capacity *= 1024 * 1024 * 1024
            elif tmp_vid_mem_multiplier == "MB":
                gpu.vram_capacity *= 1024 * 1024
            elif tmp_vid_mem_multiplier.upper() == "KB":
                gpu.vram_capacity *= 1024
            else:
                gpu.vram_capacity = -1
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

            gpu.vram_capacity = tmp_vram

            if tmp_vram_multiplier == "GB":
                gpu.vram_capacity *= 1024 * 1024 * 1024
                break
            elif tmp_vram_multiplier == "MB":
                gpu.vram_capacity *= 1024 * 1024
                break
            elif tmp_vram_multiplier.upper() == "KB":
                gpu.vram_capacity *= 1024
                break
            else:
                print("The dedicated video memory could not be found. "
                      "A video memory value will try to be found, which needs to be corrected by hand. "
                      "Ugh, humans.")

        if i == glxinfo_output_len - 1 and not dedicated_memory_found:
            if gpu.vram_capacity == -1:
                print("A dedicated video memory couldn't be found. "
                      "Value defaulted to -1. "
                      "Please humans, fix this error by hand.")
            else:
                print("A dedicated video memory couldn't be found. "
                      "A generic video memory capacity was found instead, which could be near the actual value. "
                      "Please humans, fix this error by hand.")

# SCRIPT
if has_dedicated:
    parse_lspci_output(lspci_path)
    parse_glxinfo_output(glxinfo_path)
else:
    if integrated_in_mobo:
        parse_lspci_output(lspci_path)
        # don't parse glxinfo because the VRAM is part of the RAM and varies
        gpu.vram_capacity = None
        print("The VRAM capacity could not be detected. "
              "Please try looking for it on the Video Card or on the Internet. "
              "The capacity value defaulted to 'None'."
              "For an integrated GPU, the VRAM may also be shared with the RAM, so an empty value is acceptable. ")
    else: # integrated_in_cpu
        pass
        # TODO: gather data to write code

print(gpu.brand)
print(gpu.model)
print(str(gpu.vram_capacity))

# if name == __main__:
#     read_lspci_-v_and_glxinfo()