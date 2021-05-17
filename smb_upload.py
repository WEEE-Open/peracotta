#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import shutil
from datetime import datetime


def main(parsed_args):
	try:
		load_dotenv()
		smb_path = os.environ['UPLOAD_SMB_PATH']
		smb_user = os.environ['UPLOAD_SMB_USER']
		smb_pass = os.environ['UPLOAD_SMB_PASS']
	except KeyError:
		raise EnvironmentError("Missing definition of UPLOAD_SMB_* environment variables")

	tmpdirname = "tmp_smb_mount"
	destdirname = 'peracotta-tmp-' + str(datetime.now().timestamp()).replace('.', '-')

	if os.path.isdir(tmpdirname):
		os.system(f"umount {tmpdirname}")
	else:
		os.mkdir(tmpdirname)
	os.system(f"mount -t cifs {smb_path} {tmpdirname} -o username={smb_user},password={smb_pass}")

	if parsed_args.path is None:
		path = './tmp'
	else:
		path = parsed_args.path

	if os.path.isdir(path):
		try:
			shutil.copytree(path, f"{tmpdirname}/{destdirname}", copy_function=shutil.copy)
		except shutil.Error as e:
			print(f"Copy error: {e}")
			exit(1)
		except OSError as e:
			print(f"Copy error: {e}")
			exit(1)
	else:
		print(f"Source directory {os.path.abspath(path)} is not a directory")
		exit(1)

	json = parsed_args.json
	if json is not None:
		try:
			shutil.copy(path, f"{tmpdirname}/{destdirname}")
		except shutil.Error as e:
			print(f"Copy error: {e}")
			exit(1)
		except OSError as e:
			print(f"Copy error: {e}")
			exit(1)

	print("Done!")
	exit(0)


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description="Copy files to our network share")
	parser.add_argument('path', action="store", nargs='?', type=str, help="optional path to the files directory")
	parser.add_argument('json', action="store", nargs='?', type=str, help="optional path to the json file")

	args = parser.parse_args()

	try:
		main(args)
	except KeyboardInterrupt:
		print("Keyboard interrupt, exiting")

