#!/usr/bin/env python3

import sys

# TODO: read lspci to figure out if Ethernet is 100 or 1000 or whatever
connectors_map = {
	"PS/2": "ps2-ports-n",
	"Access Bus (USB)": "usb-ports-n",
	"DB-25 male": "parallel-ports-n",
	"DB-9 male": "serial-ports-n",
	"Mini Jack (headphones)": "mini-jack-ports-n",
	"RJ-45": "ethernet-ports-n",  # not a real feature in T.A.R.A.L.L.O., since it's not yet known if it's 100 or 1000
}


class Baseboard:
	def __init__(self):
		self.type = "motherboard"
		self.brand = ""
		self.model = ""
		self.serial_number = ""
		# self.form_factor = "" # not detected by dmidecode


class Chassis:
	def __init__(self):
		self.type = "case"
		self.brand = ""
		self.model = ""
		self.serial_number = ""


# TODO: implement read of connector.txt into Baseboard

# tmp/baseboard.txt
def get_baseboard(path: str):
	mobo = Baseboard()

	# p = sp.Popen(['sudo dmidecode -t baseboard'], shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
	# out = p.communicate()
	# strings = str.split(str(out[0]), sep="\\n")

	try:
		with open(path, 'r') as f:
			output = f.read()
	except FileNotFoundError:
		print("Cannot open file.")
		print("Make sure to execute 'sudo ./generate_files.sh' first!")
		exit(-1)
		return

	for line in output.splitlines():
		if "Manufacturer" in line:
			mobo.brand = line.split("Manufacturer:")[1].strip()

		elif "Product Name" in line:
			mobo.model = line.split("Product Name:")[1].strip()

		elif "Serial Number" in line:
			mobo.serial_number = line.split("Serial Number:")[1].strip()

	result = {
		"type": mobo.type,
		"brand": mobo.brand,
		"model": mobo.model,
		"sn": mobo.serial_number,
	}

	for key, value in result.items():
		if value == "Unknown":
			del result[key]
			result[key] = None

	return result


def get_connectors(path: str, baseboard: dict):
	try:
		with open(path, 'r') as f:
			output = f.read()
	except FileNotFoundError:
		print("Cannot open file.")
		print("Make sure to execute 'sudo ./generate_files.sh' first!")
		exit(-1)
		return

	connectors = dict(zip(connectors_map.values(), [0] * len(connectors_map)))

	# TODO: this part (is it needed?)
	# port_types = []
	# devices = output.split("On Board Device")
	# for device in devices:
	# 	type = device.split("Description:")
	# 	if len(type) > 1:
	# 		port_types.append(type[1].replace("\n", "").replace(" ", ""))

	for section in output.split("\n\n"):
		if not section.startswith('Handle '):
			continue
		internal = section.split("Internal Connector Type:", 1)[1].split("\n", 1)[0].strip()
		external = section.split("External Connector Type:", 1)[1].split("\n", 1)[0].strip()
		if external == 'None':
			connector = internal
		else:
			connector = external

		if connector in connectors_map:
			connectors[connectors_map[connector]] += 1
		else:
			# TODO: save them to a warning
			print("Unknown connector: " + connector)

	for connector in connectors:
		if connectors[connector] == 0:
			del connectors[connector]

	# Dark magic: https://stackoverflow.com/a/26853961
	return {**baseboard, **connectors}

# tmp/chassis.txt
def get_chassis(path: str):
	chassis = Chassis()

	# p = sp.Popen(['sudo dmidecode -t chassis'], shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
	# out = p.communicate()
	# strings = str.split(str(out[0]), sep="\\n")

	try:
		with open(path, 'r') as f:
			output = f.read()
	except FileNotFoundError:
		print("Cannot open file.")
		print("Make sure to execute 'sudo ./generate_files.sh' first!")
		exit(-1)
		return

	for line in output.splitlines():
		if "Manufacturer" in line:
			chassis.brand = line.split("Manufacturer:")[1].strip()

		# This is Desktop, Laptop, etc...
		# TODO: use it for form factor? At least to set "proprietary-laptop" unless it's a desktop
		# elif "Type" in line:
		# chassis.model = line.split("Type:")[1].strip()

		elif "Serial Number" in line:
			chassis.serial_number = line.split("Serial Number:")[1].strip()

	result = {
		"type": chassis.type,
		"brand": chassis.brand,
		"model": chassis.model,
		"sn": chassis.serial_number
	}

	for key, value in result.items():
		if value == "Unknown":
			# Restore the default of empty string
			result[key] = ''

	return result


if __name__ == '__main__':
	while True:
		b_or_c = input("Press b for baseboard or c for chassis:\n")
		if b_or_c.lower() == "b":
			get_baseboard(sys.argv[1])
		elif b_or_c.lower() == "c":
			get_chassis(sys.argv[1])
		else:
			print("Input not recognized.")
