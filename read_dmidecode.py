#!/usr/bin/env python3

import subprocess as sp

class Baseboard:
    def __init__(self):
        self.type = ""
        self.brand = ""
        self.model = ""
        self.serial_number = ""


def get_baseboard(path: str):
    mobo = Baseboard()

    # need to set NOPASSWD: ALL in visudo
    p = sp.Popen(['sudo dmidecode -t baseboard'], shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    out = p.communicate()

    strings = str.split(str(out[0]), sep="\\n")

    for sub in strings:
        if sub.startswith("\\tManufacturer:"):
            mobo.brand = sub[16:]

        if sub.startswith("\\tProduct Name:"):
            mobo.model = sub[16:]

        if sub.startswith("\\tSerial Number:"):
            mobo.serial_number = sub[17:]

    return {
        "ty"
    }

baseboard_list = [brand, model, serial_number]
# print("baseboard_list: ", baseboard_list)


p = sp.Popen(['sudo dmidecode -t chassis'], shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
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
# print("chassis_list: ", chassis_list)
