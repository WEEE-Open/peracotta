#!/usr/bin/python3

"""
Read "lspci -v" and "glxinfo" outputs
"""

import re
import sys


class VideoCard:
	def __init__(self):
		self.type = "graphics-card"
		self.manufacturer_brand = ""
		self.reseller_brand = ""
		self.model = None
		self.capacity = -1  # bytes
		self.human_readable_capacity = ""
		self.warning = ""


def parse_lspci_output(gpu: VideoCard, lspci_path: str, interactive: bool = False):
	try:
		with open(lspci_path, 'r') as f:
			lspci_output = f.read()
	except FileNotFoundError:
		print(f"Cannot open file {lspci_path}")
		print("Make sure to execute 'sudo ./generate_files.sh' first!")
		return None
		# exit(-1)

	lspci_sections = lspci_output.split("\n\n")

	for section in lspci_sections:
		if "VGA compatible controller" in section:
			first_line = section.splitlines()[0]
			second_line = section.splitlines()[1]
			part_between_square_brackets = None
			try:
				# take the first string between [] from the first line
				part_between_square_brackets = first_line.split("[")[1].split("]")[0]
			except IndexError:
				# there may not be an argument in between []
				pass

			if 'Subsystem:' in second_line:
				# The model or model family is often repeated here, but removing it automatically is complicated
				gpu.reseller_brand = second_line.split('Subsystem: ')[1].split('[', 1)[0].strip()
				gpu.reseller_brand = gpu.reseller_brand\
					.replace('Integrated Graphics Controller', '')

			if part_between_square_brackets is not None and (
					"AMD" in part_between_square_brackets or "ATI" in part_between_square_brackets):
				gpu.manufacturer_brand = part_between_square_brackets
				# take second string between []
				gpu.model = first_line.split("[")[2].split("]")[0]
				if "controller" in gpu.model:
					gpu.model = section.splitlines()[1].split(" ")[-1]
			elif "NVIDIA" in first_line.upper():
				gpu.manufacturer_brand = "Nvidia"
				gpu.model = part_between_square_brackets
			elif "INTEL" in first_line.upper():
				gpu.manufacturer_brand = "Intel"
				if "Integrated Graphics" in first_line:
					tmp_model = first_line.split("Intel Corporation ")[1].split(" Integrated Graphics")[0]
					# if there are no numbers, e.g. "Core Processor", tmp_model is not a model number
					if not re.search("\\d+", tmp_model):
						tmp_model = ""
				elif "HD Graphics" in first_line:
					tmp_model = first_line.split("Intel Corporation ")[1].split("(", 1)[0].strip()
				elif "[" in first_line and "]" in first_line:
					tmp_model = first_line.split("[")[1].split("]")[0]
				else:
					tmp_model = ""

				if tmp_model != "":
					gpu.model = tmp_model
					gpu.reseller_brand = gpu.reseller_brand.replace(tmp_model, '').strip()
				else:
					gpu.model = None
			elif part_between_square_brackets == 'SiS':
				# May be written somewhere else on other models, but we have so few SiS cards that it's difficult to
				# find more examples. Also, they haven't made any video card in the last 15 years or so.
				gpu.manufacturer_brand = part_between_square_brackets
				if gpu.reseller_brand.lower() == 'silicon integrated systems':
					gpu.reseller_brand = 'SiS'
				gpu.model = first_line.split(']', 1)[1]
				# These may be useful for non-integrated cards, however the example ones are all integrated
				if " PCIE" in gpu.model:
					gpu.model = gpu.model.split(" PCIE", 1)[0].strip()
				elif " PCI/AGP" in gpu.model:
					gpu.model = gpu.model.split(" PCI/AGP", 1)[0].strip()
				if gpu.model in gpu.reseller_brand:
					gpu.reseller_brand = gpu.reseller_brand.split(gpu.model, 1)[0].strip()
			else:
				gpu.manufacturer_brand = None
				error = "I couldn't find the Video Card brand. The model was set to 'None' and is to be edited " \
					"logging into the TARALLO afterwards. The information you're looking for should be in the " \
					f"following 2 lines:\n{first_line}\n{second_line}\n"
				if interactive:
					print(error)
				gpu.warning += error

			if gpu.model is None:
				error = "I couldn\'t find the Integrated Graphics model. The model was set to \'None\' and is to be " \
				        "edited logging into the TARALLO afterwards. The information you\'re looking for should be in " \
					f"the following 2 lines:\n{first_line}\n{second_line}\n"
				if interactive:
					print(error)
				gpu.warning += error
			break


def parse_glxinfo_output(gpu: VideoCard, glxinfo_path: str):
	try:
		with open(glxinfo_path, 'r') as f:
			glxinfo_output = f.read()
	except FileNotFoundError:
		print(f"Cannot open file {glxinfo_path}")
		print("Make sure to execute 'sudo ./generate_files.sh' first!")
		return None
		# exit(-1)

	for i, line in enumerate(glxinfo_output.splitlines()):

		# this line comes before the "Dedicated video memory" line
		# this basically saves a default value if the dedicated memory line cannot be found
		if "Video memory" in line:
			try:
				tmp_vid_mem = int(line.split(" ")[6].split(" ")[0][:-2])
				tmp_vid_mem_multiplier = line[-2:]
			except ValueError:
				exit(-1)
				return  # To stop complaints from PyCharm

			gpu.capacity = tmp_vid_mem

			if tmp_vid_mem_multiplier == "GB":
				gpu.human_readable_capacity = str(tmp_vid_mem) + " " + tmp_vid_mem_multiplier
				gpu.capacity *= 1024 * 1024 * 1024
			elif tmp_vid_mem_multiplier == "MB":
				gpu.human_readable_capacity = str(tmp_vid_mem) + " " + tmp_vid_mem_multiplier
				gpu.capacity *= 1024 * 1024
			elif tmp_vid_mem_multiplier.upper() == "KB":
				gpu.human_readable_capacity = str(tmp_vid_mem) + " " + tmp_vid_mem_multiplier
				gpu.capacity *= 1024
			else:
				gpu.capacity = -1
				# print("The VRAM capacity could not be detected. "
				#       "Please try looking for it on the Video Card or on the Internet. "
				#       "The detected value defaulted to -1.")

		if "Dedicated video memory" in line:

			try:
				tmp_vram = int(line.split(" ")[7].split(" ")[0])
				tmp_vram_multiplier = line[-2:]
			except ValueError:
				exit(-1)
				return

			gpu.capacity = tmp_vram

			if tmp_vram_multiplier == "GB":
				gpu.human_readable_capacity = str(tmp_vram) + " " + tmp_vram_multiplier
				gpu.capacity *= 1024 * 1024 * 1024
				break
			elif tmp_vram_multiplier == "MB":
				gpu.human_readable_capacity = str(tmp_vram) + " " + tmp_vram_multiplier
				gpu.capacity *= 1024 * 1024
				break
			elif tmp_vram_multiplier.upper() == "KB":
				gpu.human_readable_capacity = str(tmp_vram) + " " + tmp_vram_multiplier
				gpu.capacity *= 1024
				break
			else:
				gpu.capacity = -1
				gpu.warning = "Could not find dedicated video memory. Please check the value."


def read_lspci_and_glxinfo(has_dedicated: bool, lspci_path: str, glxinfo_path: str, interactive: bool = False):
	gpu = VideoCard()
	if has_dedicated:
		parse_lspci_output(gpu, lspci_path, interactive)
		parse_glxinfo_output(gpu, glxinfo_path)
	else:  # integrated_in_mobo or integrated_in_cpu
		parse_lspci_output(gpu, lspci_path, interactive)
		# don't parse glxinfo because the VRAM is part of the RAM and varies
		gpu.capacity = None
		# print("The VRAM capacity could not be detected. "
		# "Please try looking for it on the Video Card or on the Internet. "
		# "The capacity value defaulted to 'None'. "
		# "For an integrated GPU, the VRAM may also be shared with the system RAM, so an empty value is acceptable.")

	result = {
		"type": "graphics-card",
		"brand": gpu.reseller_brand,
		"model": gpu.model,
		"capacity-byte": gpu.capacity,
		"human_readable_capacity": gpu.human_readable_capacity
	}
	if gpu.manufacturer_brand.lower() != gpu.reseller_brand.lower():
		result["brand-manufacturer"] = gpu.manufacturer_brand
	return result


if __name__ == '__main__':
	while True:
		ded = input("Does this system have a dedicated GPU? y/n:\n")
		if ded.lower() == "y":
			read_lspci_and_glxinfo(True, sys.argv[1], sys.argv[2], True)
		elif ded.lower() == "n":
			read_lspci_and_glxinfo(False, sys.argv[1], sys.argv[2], True)
		else:
			print("Unexpected character.")
