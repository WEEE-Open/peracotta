# TODO: delete read dmidecode (already done) and separate and elaborate read_lscpu

#!/usr/bin/env python3
import sys

filepath = sys.argv[1]

'''
Read "dmidecode -t baseboard" output:
'''

f = open(filepath + '/baseboard.txt', 'r')

if f == 0:
    print("cannot open file")
    print("Make sure to execute 'sudo ./generate_files.sh' first!")
    exit(0)


print("reading dmidecode -t baseboard...")

brand = ""
model = ""
serial_number = ""
n_ports = 0
port_types = []

output = f.read()
# print(output)

strings = output.splitlines()

# print("strings: ", strings)


for sub in strings:
    if sub.startswith("\tManufacturer:"):
        brand = sub[15:]

    if sub.startswith("\tProduct Name:"):
        model = sub[15:]

    if sub.startswith("\tSerial Number:"):
        serial_number = sub[16:]

devices = output.split("On Board Device")
for device in devices:
    type = device.split("Description:")
    if type.__len__() > 1:
        port_types.append(type[1].replace("\n", "").replace(" ", ""))

baseboard_list = {'Brand': brand, 'Model': model, 'Serial Number': serial_number}
print("baseboard_list: ", baseboard_list)

print("port_number: ", port_types.__len__())
print("port_types: ", port_types)
print()
f.close()

'''
Read "dmidecode -t chassis" output:
'''

f = open('chassis.txt', 'r')

if f == 0:
    print("cannot open file")
    exit(0)


print("reading dmidecode -t chassis...")

brand = ""
model = ""
serial_number = ""

output = f.read()

strings = output.splitlines()

# print("strings: ", strings)


for sub in strings:
    if sub.startswith("\tManufacturer:"):
        brand = sub[15:]

    if sub.startswith("\tType:"):
        model = sub[7:]

    if sub.startswith("\tSerial Number:"):
        serial_number = sub[16:]

chassis_list = {'Brand': brand, 'Model': model, 'Serial Number': serial_number}
print("chassis_list: ", chassis_list)
print()
f.close()

'''
Read "lscpu" output
'''
print("Reading lscpu...")

f = open('lscpu.txt', 'r')

if f == 0:
    print("cannot open file")
    exit(0)

architecture = ""
brand = ""
model = ""
frequency = ""
n_cores = ""

cpu_info = {}

output = f.read()

strings = output.splitlines()
for sub in strings:
    if sub.startswith("Architecture:"):
        architecture = sub.replace("Architecture:", "").replace(" ", "")

    if sub.startswith("Model name:"):
        model = sub.replace("Model name:", "").replace(" ", "")

    if sub.startswith("Vendor ID:"):
        brand = sub.replace("Vendor ID:", "").replace(" ", "")

    if sub.startswith("Core(s) per socket:"):
        n_cores = sub.replace("Core(s) per socket:", "").replace(" ", "")

cpu_info['Architecture'] = architecture
cpu_info['Model'] = model
cpu_info['Vendor'] = brand
cpu_info['N.cores'] = n_cores

print(cpu_info)
print()
