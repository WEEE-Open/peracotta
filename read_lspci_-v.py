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

# ASK THE USER
has_dedicated = None
while True:
    dedicated = input("Does this system have a dedicated video card? Y/N")
    if dedicated.lower() == "y":
        has_dedicated = True
        break
    elif dedicated.lower() == "n":
        has_dedicated = False
        break
    else:
        print("Please enter 'Y' or 'N'")
        continue

if has_dedicated:
    f = open("tests/asdpc/lspci")
else:
    pass
# TODO: write code