#!/usr/bin/env python3
import sys

'''
Read "decode-dimms" output:
This script is based on read_dmidecode.py
'''

class Dimm:
    def __init__(self):
        self.type = "RAM"
        self.brand = ""
        self.model = ""
        self.serial_number = ""
        self.frequency = -1
        self.frequency_multiplier = ""
        self.capacity = -1
        self.capacity_multiplier = ""
        self.RAM_type = ""  # DDR, DDR2, DDR3 etc.
        self.ECC = ""  # enum: "Yes" or "No"
        self.CAS_latency = ""  # feature not yet implemented on TARALLO
        self._manufacturer_data_type = ""

# TODO: revert to original state
# filepath = sys.argv[1]
# f = open(filepath + '/dimms.txt', 'r')
f = open("/Users/Caste/Documents/WEEEOpen/peracotta/tests/asdpc/dimms.txt", 'r')

if f == 0:
    print("Cannot open file.")
    print("Make sure to execute 'sudo ./generate_files.sh' first!")
    exit(-1)

print("Reading decode-dimms...")

output = f.read()
# print(output)
f.close()

# this optimization can crash the script if output is empty
# last_line = output.splitlines()[-1]

# check based on output of decode-dimms v6250
if "Number of SDRAM DIMMs detected and decoded: 0" in output \
        or "Number of SDRAM DIMMs detected and decoded: " not in output:
    print("decode-dimms was not able to find any RAM details")
    exit(-1)

# split strings in 1 str array for each DIMM
dimm_sections = output.split("Decoding EEPROM")
# remove useless first part
del dimm_sections[0]
# for dimm in dimm_sections:
#     print(dimm)
#     print("END OF THIS ENTRY")
# exit(0)

# create list of as many dimms as there are dimm_sections
dimms = [Dimm() for i in range(len(dimm_sections))]

i = 0
for dimm in dimm_sections:
    for line in dimm.splitlines():
        if line.startswith("Fundamental Memory type"):
            dimms[i].RAM_type = line.split(" ")[-2]

        if line.startswith("Maximum module speed"):
            freq = line.split(" ")[-3:-1]
            # can RAM frequencies be in any other unit than MHz?
            if "MHz" in freq[1]:
                dimms[i].frequency_multiplier = "M"
            elif "GHz" in freq[1]:
                dimms[i].frequency_multiplier = "G"
            elif "KHz" in freq[1] or "kHz" in freq[1]:
                dimms[i].frequency_multiplier = "K"
            dimms[i].frequency = int(freq[0])

        if line.startswith("Size"):
            cap = line.split(" ")[-2:]
            dimms[i].capacity = int(cap[0])
            if "MB" in cap[1]:
                dimms[i].capacity_multiplier = "M"
            elif "GB" in cap[1]:
                dimms[i].capacity_multiplier = "G"
            elif "KB" in cap[1] or "kB" in cap[1]:
                dimms[i].capacity_multiplier = "K"

        # alternatives to "Manufacturer" are "DRAM Manufacturer" and "Module Manufacturer"
        if "---=== Manufacturer Data ===---" in line:
            dimms[i]._manufacturer_data_type = "DRAM Manufacturer"

        if "---=== Manufacturing Information ===---" in line:
            dimms[i]._manufacturer_data_type = "Manufacturer"

        if line.startswith(dimms[i]._manufacturer_data_type):
            if dimms[i]._manufacturer_data_type == "DRAM Manufacturer":
                relevant_part = line[17:]
                while relevant_part.startswith(" "):
                    relevant_part = relevant_part[1:]
                dimms[i].brand = relevant_part
            elif dimms[i]._manufacturer_data_type == "Manufacturer":
                relevant_part = line[12:]
                while relevant_part.startswith(" "):
                    relevant_part = relevant_part[1:]
                dimms[i].brand = relevant_part

    # proceed to next dimm
    i += 1

for dimm in dimms:
    print("----------------------------")
    print(dimm.RAM_type)
    print(str(dimm.frequency) + dimm.frequency_multiplier)
    print(str(dimm.capacity) + dimm.capacity_multiplier)
    print(dimm.brand)
