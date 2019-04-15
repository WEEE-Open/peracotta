#!/usr/bin/env python3

"""
Read "lspci -v" output
"""

class VideoCard:
    def __init__(self):
        self.type = "graphics-card"
        self.brand = ""
        self.model = ""
        self.vram_capacity = -1 # int
        self.vram_capacity_mulitplier = ""

# ASK THE USER
has_dedicated = None
integrated_in_mobo = None
while True:
    dedicated = input("Does this system have a dedicated video card? Y/N: ")
    if dedicated.lower() == "y":
        has_dedicated = True
        break
    elif dedicated.lower() == "n":
        has_dedicated = False
        while True:
            where_is_integrated = input("Is the video card integrated in the motherboard (press M)"
                                       " or in the CPU (press C)? Tip: the older the system,"
                                       " the higher the chance the GPU is integrated in the"
                                       " motherboard.")
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
asdpc = 1
jm11 = 0
polveroso = 0
rottame = 0
workstation = 0
if asdpc:
    test_output = "asdpc"
elif jm11:
    test_output = "jm11"
elif polveroso:
    test_output = "polveroso"
elif rottame:
    test_output = "rottame"
else: # workstation:
    test_output = "workstation"
"""END TEST"""

# SCRIPT
if has_dedicated:
    try:
        with open("tests/" + test_output + "/lspci.txt") as f:
            print("Reading lspci -v...")
            output = f.read()
    except FileNotFoundError as fnfe:
        print("Cannot open file.")
        print("Make sure to execute 'sudo ./generate_files.sh' first!")
        exit(-1)

    sections = output.split("\n\n")

    for section in sections:
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
                    # TODO: are there other brands other than AMD/ATI and NVIDIA?
                    pass

            for line in section.splitlines():
                # only considering prefetchable VRAM
                if "Memory" in line and "non" not in line and "prefetchable" in line:
                    vram = line.split("size=")[1].split("]")[0]
                    if vram[-1].upper() == "M":
                        gpu.vram_capacity_mulitplier = "M"
                    elif vram[-1].upper() == "K":
                        gpu.vram_capacity_mulitplier = "K"
                    elif vram[-1].upper() == "G":
                        gpu.vram_capacity_mulitplier = "G"
                    else:
                        pass
                        # TODO: throw OhMyGodIsThisVRAMInTerabytesException
                    gpu.vram_capacity = int(vram[:-1])


else:
    if integrated_in_mobo:
        pass
    else: # integrated_in_cpu
        pass
        # TODO: write code

print(gpu.brand)
print(gpu.model)
print(str(gpu.vram_capacity) + gpu.vram_capacity_mulitplier)