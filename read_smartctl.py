#!/usr/bin/env python3
import sys
import os
from math import log10, floor


"""
Read "smartctl" output:
"""


class Disk:
	def __init__(self):
		self.type = ""
		self.brand = ""
		self.model = ""
		self.family = ""
		self.wwn = ""
		self.serial_number = ""
		self.capacity = -1  # n of bytes
		self.human_readable_capacity = ""
		self.rotation_rate = -1
		self.smart_data = False


# THE PATH HERE ONLY POINTS TO THE DIRECTORY, eg. tmp, AND NOT TO THE FILE, e.g. tmp/smartctl-dev-sda.txt,
# SINCE THERE MAY BE MULTIPLE FILES
def read_smartctl(path: str, interactive: bool = False):
	try:
		disks = []

		for filename in os.listdir(path):
			if "smartctl-dev-" in filename:

				disk = Disk()

				with open(path + "/" + filename, 'r') as f:
					output = f.read()

				if '=== START OF INFORMATION SECTION ===' not in output:
					if interactive:
						print(f"{filename} does not contain disk information, was it a USB stick?")
					continue

				data = output.split('=== START OF INFORMATION SECTION ===', 1)[1]\
					.split('=== START OF READ SMART DATA SECTION ===', 1)[0]

				# For manual inspection later on
				disk.smart_data = '=== START OF READ SMART DATA SECTION ===' +\
					output.split('=== START OF READ SMART DATA SECTION ===', 1)[1]

				for line in data.splitlines():
					if "Model Family" in line:
						line = line.split("Model Family:")[1].strip()
						if line.startswith('Western Digital'):
							disk.brand = 'Western Digital'
							disk.family = line.split('Western Digital', 1)[1].strip()
						elif line.startswith('Samsung'):
							disk.brand = 'Samsung'
							disk.family = line.split('Samsung', 1)[1].strip()
						# TODO: elif for other brands
						else:
							disk.brand = line
					elif "Device Model" in line:
						disk.model = line.split("Device Model:")[1].strip()
					elif "Serial Number" in line:
						disk.serial_number = line.split("Serial Number:")[1].strip()

					elif "LU WWN Device Id" in line:
						disk.wwn = line.split("LU WWN Device Id:")[1].strip()

					elif "User Capacity" in line:
						# https://stackoverflow.com/a/3411435
						num_bytes = line.split('User Capacity:')[1].split("bytes")[0].strip().replace(',', '')
						round_digits = int(floor(log10(abs(float(num_bytes))))) - 2
						bytes_rounded = int(round(float(num_bytes), - round_digits))
						disk.capacity = bytes_rounded

						tmp_capacity = line.split("[")[1].split("]")[0]
						if tmp_capacity is not None:
							disk.human_readable_capacity = tmp_capacity

					elif "Rotation Rate" in line:
						if "Solid State Device" not in line:
							disk.rotation_rate = int(line.split("Rotation Rate:")[1].split("rpm")[0].strip())
							disk.type = "hdd"
						else:
							disk.type = "ssd"

				if disk.brand == 'Western Digital':
					# These are useless and usually not even printed on labels and in bar codes...
					disk.model = remove_prefix('WDC ', disk.model)
					disk.serial_number = remove_prefix('WD-', disk.serial_number)

				disks.append(disk)

		result = []
		for disk in disks:
			if disk.type == "hdd":
				result.append({
					"type": "hdd",
					"brand": disk.brand,
					"model": disk.model,
					"family": disk.family,
					"wwn": disk.wwn,
					"sn": disk.serial_number,
					# Despite the name it's still in bytes, but with SI prefix (not power of 2), "deci" is there just to
					# tell some functions how to convert it to human-readable format
					"capacity-decibyte": disk.capacity,
					"human_readable_capacity": disk.human_readable_capacity,
					"spin-rate-rpm": disk.rotation_rate,
					"smart-data": disk.smart_data
				})
			else:  # ssd
				result.append({
					"type": "ssd",
					"brand": disk.brand,
					"model": disk.model,
					"family": disk.family,
					"sn": disk.serial_number,
					"capacity-byte": disk.capacity,
					"human_readable_capacity": disk.human_readable_capacity,
					"smart-data": disk.smart_data
				})

		return result

	except FileNotFoundError:
		print("Cannot open file.")
		print("Make sure to execute 'sudo ./generate_files.sh' first!")
		exit(-1)


def remove_prefix(prefix, text):
	if text.startswith(prefix):
		return text[len(prefix):]
	return text


if __name__ == '__main__':
	print(read_smartctl(sys.argv[1], True))
