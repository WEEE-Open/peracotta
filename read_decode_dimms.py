#!/usr/bin/python3

'''
Read "decode-dimms" output
'''

class Dimm:
    def __init__(self):
        self.type = "ram"
        self.brand = ""
        self.model = ""
        self.serial_number = ""
        self.frequency = -1
        self.human_readable_frequency = ""
        self.capacity = -1
        self.human_readable_capacity = ""
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

"""START TEST"""
asdpc = 0
rottame = 0
ECC1 = 0
ECC2 = 0
_149 = 0
if asdpc:
    path = "tests/asdpc/dimms.txt"
elif rottame:
    path = "tests/rottame/dimms.txt"
elif ECC1:
    path = "tests/decode-dimms/ECC/R451-R450.txt"
elif ECC2:
    path = "tests/decode-dimms/ECC/R480-R479.txt"
elif _149:
    path = "tests/decode-dimms/non ECC/R469-R470-R471-R472.txt"
else:
    path = ""
"""END TEST"""

def read_decode_dimms(path: str):
    print(path)
    try:
        with open(path, 'r') as f:
            output = f.read()
    except FileNotFoundError:
        print("Cannot open file.")
        print("Make sure to execute 'sudo ./generate_files.sh' first!")
        exit(-1)

    # print("Reading decode-dimms...")

    # this optimization can crash the script if output is empty
    # last_line = output.splitlines()[-1]

    # check based on output of decode-dimms v6250
    if "Number of SDRAM DIMMs detected and decoded: 0" in output \
            or "Number of SDRAM DIMMs detected and decoded: " not in output:
        # TO USE WITH extract_data.py
        print("decode-dimms was not able to find any RAM details")
        return None
        # exit(-1)

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

    for i, dimm in enumerate(dimm_sections):
        for line in dimm.splitlines():
            if line.startswith("Fundamental Memory type"):
                dimms[i].RAM_type = line.split(" ")[-2]

            if line.startswith("Maximum module speed"):
                freq = line.split(" ")[-3:-1]
                dimms[i].frequency = int(freq[0])
                if "KHz" in freq[1] or "kHz" in freq[1]:
                    dimms[i].human_readable_frequency = freq[0] + " KHz"
                    dimms[i].frequency *= 1000
                elif "MHz" in freq[1]:
                    dimms[i].human_readable_frequency = freq[0] + " MHz"
                    dimms[i].frequency *= 1000*1000
                elif "GHz" in freq[1]:
                    dimms[i].human_readable_frequency = freq[0] + " GHz"
                    dimms[i].frequency *= 1000*1000*1000

            if line.startswith("Size"):
                cap = line.split(" ")[-2:]
                dimms[i].capacity = int(cap[0])
                if "KB" in cap[1] or "kB" in cap[1]:
                    dimms[i].human_readable_capacity = cap[0] + " KB"
                    dimms[i].capacity *= 1024
                elif "MB" in cap[1]:
                    dimms[i].human_readable_capacity = cap[0] + " MB"
                    dimms[i].capacity *= 1024*1024
                elif "GB" in cap[1]:
                    dimms[i].human_readable_capacity = cap[0] + " GB"
                    dimms[i].capacity *= 1024*1024*1024

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

            # TODO: fix that it never finds the model
            # is part number the model?
            if line.startswith("Part Number") and dimms[i].serial_number == "":
                dimms[i].serial_number = ignore_spaces(line, len("Part Number"))

            # part number can be overwritten by serial number if present
            if line.startswith("Assembly Serial Number"):
                dimms[i].serial_number = ignore_spaces(line, len("Assembly Serial Number"))

            if line.startswith("Module Configuration Type") and \
                    ("Data Parity" in line
                    or "Data ECC" in line
                    or "Address/Command Parity" in line):
                dimms[i].ECC = "Yes"

            if line.startswith("Supported CAS Latencies (tCL)"):
                dimms[i].CAS_latencies = ignore_spaces(line, len("Supported CAS Latencies (tCL)"))

    # TODO: comment following lines in production code
    # for dimm in dimms:
    #     print("-"*25)
    #     print(dimm.RAM_type)
    #     print(str(dimm.frequency))
    #     print(str(dimm.capacity))
    #     print(dimm.brand)
    #     print(dimm.serial_number)
    #     print(dimm.ECC)
    #     print(dimm.CAS_latencies)

    dimms_dicts = []
    for dimm in dimms:
        dimms_dicts.append({
            "type": "ram",
            "brand": dimm.brand,
            "model": dimm.model,
            "serial_number": dimm.serial_number,
            "frequency": dimm.frequency,
            "human_readable_frequency": dimm.human_readable_frequency,
            "capacity": dimm.capacity,
            "human_readable_capacity": dimm.human_readable_capacity,
            "RAM_type": dimm.RAM_type,
            "ECC": dimm.ECC
            # "CAS_latencies": dimm.CAS_latencies,# feature not yet implemented on TARALLO
        })

    return dimms_dicts

if __name__ == '__main__':
    read_decode_dimms(path)