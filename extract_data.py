#!/usr/bin/env python3

"""
Collect data from all the 'read...' scripts and returns it as a list of dicts
"""
import json

from read_dmidecode import get_baseboard, get_chassis, get_connectors, get_net
from read_lscpu import read_lscpu
from read_decode_dimms import read_decode_dimms
from read_lspci_and_glxinfo import read_lspci_and_glxinfo
from read_smartctl import read_smartctl


def extract_and_collect_data_from_generated_files(directory: str, has_dedicated_gpu: bool, interactive: bool = False):
	directory = directory.rstrip('/')

	chassis, cpu, dimms, disks, gpu, mobo = extract_data(directory, has_dedicated_gpu, interactive)

	# TODO: add mobo, chassis, cpu, disks checks

	no_dimms_str = "decode-dimms was not able to find any RAM details"

	# the None check MUST come before the others
	if dimms is None or no_dimms_str in dimms:
		# empty default dictionary
		dimms = {
			"type": "ram",
			"brand": None,
			"model": None,
			"serial_number": None,
			"frequency": None,
			"human_readable_frequency": None,
			"capacity": None,
			"human_readable_capacity": None,
			"RAM_type": None,
			"ECC": None
			# "CAS_latencies": None # feature missing from TARALLO
		}

	no_gpu_info_str = "I couldn't find the Video Card brand. The model was set to 'None' and is to be edited logging " \
	                  "into the TARALLO afterwards. The information you're looking for should be in the following 2 lines:"
	no_vram_info_str = "A dedicated video memory couldn't be found. A generic video memory capacity was found instead, which " \
	                   "could be near the actual value. Please humans, fix this error by hand."

	if gpu is None or (no_gpu_info_str in gpu and no_vram_info_str in gpu):
		gpu = {
			"type": "graphics-card",
			"manufacturer_brand": None,
			"reseller_brand": None,
			"model": None,
			"capacity": None,
			"human_readable_capacity": None
		}
		print_lspci_lines_in_dialog = True

	elif no_vram_info_str in gpu and no_gpu_info_str not in gpu:
		# TODO: check output in this case, change only VRAM field to None
		print_lspci_lines_in_dialog = False

	else:
		print_lspci_lines_in_dialog = False

	result = [chassis, mobo, cpu]

	if isinstance(dimms, dict):
		# otherwise it will append every key-value pair of the dict
		result.append(dimms)
	else:
		for dimm in dimms:
			result.append(dimm)

	# assuming there is only 1 graphics card in the system
	result.append(gpu)

	if isinstance(disks, dict):
		result.append(disks)
	else:
		for disk in disks:
			result.append(disk)

	# tuple = list(dicts), bool
	return result, print_lspci_lines_in_dialog


def extract_data(directory, has_dedicated_gpu, interactive):
	mobo = get_baseboard(directory + "/baseboard.txt")
	mobo = get_connectors(directory + "/connector.txt", mobo, interactive)
	mobo = get_net(directory + "/net.txt", mobo, interactive)
	chassis = get_chassis(directory + "/chassis.txt")
	cpu = read_lscpu(directory + "/lscpu.txt")
	dimms = read_decode_dimms(directory + "/dimms.txt", interactive)
	gpu = read_lspci_and_glxinfo(has_dedicated_gpu, directory + "/lspci.txt", directory + "/glxinfo.txt", interactive)
	disks = read_smartctl(directory)

	result = []
	for thing in (mobo, chassis, cpu, dimms, disks, gpu, mobo):
		if isinstance(thing, list):
			result += thing
		else:
			result.append(thing)
	return result


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Get all the possible output data things")
	parser.add_argument('-s', '--short', action="store_true", default=False, help="print shorter ouput")
	parser.add_argument('-g', '--gpu', action="store_true", default=False, help="computer has dedicated GPU")
	parser.add_argument('path', action="store", nargs='?', type=str, help="to directory with txt files")
	args = parser.parse_args()

	if args.path is None:
		path = '.'
	else:
		path = args.path

	if args.short:
		print(json.dumps(extract_data(path, args.gpu, False), indent=2))
	else:
		print(json.dumps(extract_and_collect_data_from_generated_files(path, args.gpu, True), indent=2))
