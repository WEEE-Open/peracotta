#!/usr/bin/env python3
import sys
import os

# if sys.argv.__len__() < 1:
#     print("Invalid call, specify filename to read")
#     exit(0)


"""
Read "smartctl" output:
"""


class Disk:
	def __init__(self):
		self.type = ""
		self.brand = ""
		self.model = ""
		self.wwn = ""
		self.serial_number = ""
		self.capacity = -1  # n of bytes
		self.human_readable_capacity = ""
		self.rotation_rate = -1
		self.smart_data = False


# THE PATH HERE ONLY POINTS TO THE DIRECTORY, eg. tmp, AND NOT TO THE FILE, e.g. tmp/smartctl-dev-sda.txt,
# SINCE THERE MAY BE MULTIPLE FILES
def read_smartctl(path: str):
	try:
		disks = []

		for filename in os.listdir(path):
			if "smartctl-dev-" in filename:

				disk = Disk()

				with open(path + "/" + filename, 'r') as f:
					output = f.read()

				for line in output.splitlines():
					if "Model Family" in line:
						disk.brand = line.split("Model Family:")[1].strip()

					elif "Device Model" in line:
						disk.model = line.split("Device Model:")[1].strip()

					elif "Serial Number" in line:
						disk.serial_number = line.split("Serial Number:")[1].strip()

					elif "LU WWN Device Id" in line:
						disk.wwn = line.split("LU WWN Device Id:")[1].strip()

					elif "User Capacity" in line:
						tmp_capacity = line.split("[")[1].split("]")[0]
						if tmp_capacity is not None:
							disk.human_readable_capacity = tmp_capacity
							if "GB" in tmp_capacity:
								disk.capacity = int(tmp_capacity[:-2]) * 1024 * 1024 * 1024

							elif "MB" in tmp_capacity:
								disk.capacity = int(tmp_capacity[:-2]) * 1024 * 1024

							elif "KB" in tmp_capacity.upper():
								disk.capacity = int(tmp_capacity[:-2]) * 1024

					elif "Rotation Rate" in line:
						if "Solid State Device" not in line:
							disk.rotation_rate = int(line.split("Rotation Rate:")[1].split("rpm")[0].strip())
							disk.type = "hdd"
						else:
							disk.type = "ssd"

					elif "SMART support is" in line:
						if "Available" in line or "Enabled" in line:
							disk.smart_data = True

				disks.append(disk)

		result = []
		for disk in disks:
			if disk.type == "hdd":
				result.append({
					"type": "hdd",
					"brand": disk.brand,
					"model": disk.model,
					"wwn": disk.wwn,
					"sn": disk.serial_number,
					"capacity-decibyte": int(disk.capacity / 10),
					"human_readable_capacity": disk.human_readable_capacity,
					"spin-rate-rpm": disk.rotation_rate,
					"smart-data": disk.smart_data
				})
			else:  # ssd
				result.append({
					"type": "ssd",
					"brand": disk.brand,
					"model": disk.model,
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


if __name__ == '__main__':
	print(read_smartctl(sys.argv[1]))
