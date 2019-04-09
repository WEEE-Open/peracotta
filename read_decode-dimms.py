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
        self.ECC = "No"  # enum: "Yes" or "No"
        self.CAS_latencies = ""  # feature not yet implemented on TARALLO
        self._manufacturer_data_type = ""

# initial_chars_to_ignore is the length of the feature whose name the line begins with
# e.g. "Fundamental Memory Type" begins with 23 characters that are not all spaces, then n spaces to ignore,
# and finally there's the value needed, e.g. "DDR3 SDRAM"
def ignore_spaces(line:str, initial_chars_to_ignore:int):
    relevant_part = line[initial_chars_to_ignore:]
    return relevant_part.strip()

# TODO: revert to original state
# filepath = sys.argv[1]
# f = open(filepath + '/dimms.txt', 'r')

"""START TEST"""
asdpc = False
rottame = False
ECC1 = False
ECC2 = False
_149 = True
if asdpc:
    f = open("tests/asdpc/dimms.txt", 'r')
elif rottame:
    f = open("tests/rottame/dimms.txt", 'r')
elif ECC1:
    f = open("tests/decode-dimms/ECC/R451-R450.txt", 'r')
elif ECC2:
    f = open("tests/decode-dimms/ECC/R480-R479.txt", 'r')
elif _149:
    f = open("tests/decode-dimms/non ECC/R469-R470-R471-R472.txt", 'r')
"""END TEST"""


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
                dimms[i].brand = ignore_spaces(line, len("DRAM Manufacturer"))
            elif dimms[i]._manufacturer_data_type == "Manufacturer":
                dimms[i].brand = ignore_spaces(line, len("Manufacturer"))

        # is part number the model?
        if line.startswith("Part Number") and dimms[i].serial_number == "":
            # dimms[i].serial_number = line.split(" ")[-1]
            dimms[i].serial_number = ignore_spaces(line, len("Part Number"))

        # part number can be overwritten by serial number if present
        if line.startswith("Assembly Serial Number"):
            # dimms[i].serial_number = line.split(" ")[-1]
            dimms[i].serial_number = ignore_spaces(line, len("Assembly Serial Number"))

        if line.startswith("Module Configuration Type") and \
                ("Data Parity" in line
                or "Data ECC" in line
                or "Address/Command Parity" in line):
            dimms[i].ECC = "Yes"

        if line.startswith("Supported CAS Latencies (tCL)"):
            dimms[i].CAS_latencies = ignore_spaces(line, len("Supported CAS Latencies (tCL)"))

    # proceed to next dimm
    i += 1

for dimm in dimms:
    print("-"*25)
    print(dimm.RAM_type)
    print(str(dimm.frequency) + dimm.frequency_multiplier)
    print(str(dimm.capacity) + dimm.capacity_multiplier)
    print(dimm.brand)
    print(dimm.serial_number)
    print(dimm.ECC)
    print(dimm.CAS_latencies)

# TODO: return all the dimms to caller script otherwise this thing is utterly useless