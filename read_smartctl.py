#!/usr/bin/env python3
import sys

if sys.argv.__len__() < 1:
    print("Invalid call, specify filename to read")
    exit(0)

filepath = sys.argv[1]

'''
Read "smartctl" output:
'''

f = open(filepath, 'r')

if f == 0:
    print("cannot open file")
    print("Make sure to execute 'sudo ./generate_files.sh' first!")
    exit(0)


brand = ""
model = ""
wwn = ""
serial_number = ""
capacity = 0  # n of bytes
rotation_rate = ""

output = f.read()
# print(output)

strings = output.splitlines()

for sub in strings:
    if sub.startswith("Model Family:"):
        brand = sub[18:]

    if sub.startswith("Device Model:"):
        model = sub[18:]

    if sub.startswith("Serial Number:"):
        serial_number = sub[18:]

    if sub.startswith("LU WWN Device Id:"):
        wwn = sub[20:26]

    if sub.startswith("User Capacity:"):
        capacity = sub[18:]
        capacity_list = capacity.split(" ")
        capacity = capacity_list[0] + " " + capacity_list[1]

    if sub.startswith("Rotation Rate:"):
        rotation_rate = sub[18:]


smartctl_list = {'Brand': brand, 'Model': model, 'Serial Number': serial_number, 'WWN': wwn, 'Capacity': capacity, 'Rotation_rate': rotation_rate}
print("baseboard_list: ", smartctl_list)

print()
f.close()
