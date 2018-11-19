import subprocess

print("DMIDECODE output: ")

# need to set NOPASSWD: ALL in visudo
p = subprocess.Popen(['sudo dmidecode -t baseboard'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out = p.communicate()

# p = subprocess.call(['dmidecode', '-t', 'baseboard'])

# print("out[0] contains: ")
# print(out[0])

brand = ""
model = ""
serial_number = ""
strings = str.split(str(out[0]), sep="\\n")

for sub in strings:
    if sub.startswith("\\tManufacturer:"):
        brand = sub[16:]

    if sub.startswith("\\tProduct Name:"):
        model = sub[16:]

    if sub.startswith("\\tSerial Number:"):
        serial_number = sub[17:]

baseboard_list = [brand, model, serial_number]
print("baseboard_list: ", baseboard_list)


p = subprocess.Popen(['sudo dmidecode -t chassis'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out = p.communicate()

brand = ""
model = ""
serial_number = ""
strings = str.split(str(out[0]), sep="\\n")

for sub in strings:
    if sub.startswith("\\tManufacturer:"):
        brand = sub[16:]

    if sub.startswith("\\tType:"):
        model = sub[8:]

    if sub.startswith("\\tSerial Number:"):
        serial_number = sub[17:]

chassis_list = [brand, model, serial_number]
print("chassis_list: ", chassis_list)
