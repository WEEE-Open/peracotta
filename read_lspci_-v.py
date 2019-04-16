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
    except FileNotFoundError:
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

            for line in section.splitlines():
                # only considering prefetchable VRAM
                if "Memory" in line and "non" not in line and "prefetchable" in line:
                    vram = line.split("size=")[1].split("]")[0]
                    last_char = vram[-1].upper()
                    size = int(vram[:-1])

                    # selects biggest prefetchable memory
                    if gpu.vram_capacity < size:
                        gpu.vram_capacity = size
                    else:
                        break

                    if last_char == "M":
                        gpu.vram_capacity_mulitplier = "M"
                    elif last_char == "K":
                        gpu.vram_capacity_mulitplier = "K"
                    elif last_char == "G":
                        gpu.vram_capacity_mulitplier = "G"
                    else:
                        while True:
                            tmp = input("I couldn't find the VRAM Capacity. Please check the VRAM (Video Memory) of the card"
                                        " and enter it below: \nformat: <integer><K/M/G for Kilobytes/Megabytes/Gigabytes\n"
                                        "e.g. 256M\n")
                            multiplier = tmp[-1].upper()
                            mult_full = ""
                            if multiplier == "K":
                                mult_full = "Kilobytes"
                            elif multiplier == "M":
                                mult_full = "Megabytes"
                            elif multiplier == "G":
                                mult_full = "Gigabytes"
                            else:
                                print("Unrecognized format. Please try again.")
                                continue

                            try:
                                size = int(tmp[:-1])
                            except ValueError:
                                print("Unrecognized format. Please try again.")
                                continue

                            confirm = input("Confirm the VRAM has a capacity of " + str(size) + " " + mult_full + " Y/N\n")
                            if confirm.lower() == "y":
                                gpu.vram_capacity = size
                                gpu.vram_capacity_mulitplier = multiplier
                                break
                            else:
                                print("Enter a new value.")
                                continue

            break


else:
    if integrated_in_mobo:
        pass
    else: # integrated_in_cpu
        pass
        # TODO: write code

print(gpu.brand)
print(gpu.model)
print(str(gpu.vram_capacity) + gpu.vram_capacity_mulitplier)