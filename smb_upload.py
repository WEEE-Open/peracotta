#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import shutil
from datetime import datetime


def main(parsed_args):
    try:
        load_dotenv()
        smb_path = os.environ["UPLOAD_SMB_PATH"]
        smb_user = os.environ["UPLOAD_SMB_USER"]
        smb_pass = os.environ["UPLOAD_SMB_PASS"]
    except KeyError:
        raise EnvironmentError(
            "Missing definition of UPLOAD_SMB_* environment variables"
        )

    tmpdirname = "/tmp/peracotta_smb_mount"
    destdirname = "peracotta-tmp-" + str(datetime.now().timestamp()).replace(".", "-")

    if not os.path.isdir(tmpdirname):
        os.mkdir(tmpdirname)

    json = parsed_args.json
    if parsed_args.path is None:
        path = "/home/weee/peracotta/tmp"
    else:
        path = parsed_args.path

    try:
        os.system(
            f"sudo mount -t cifs {smb_path} {tmpdirname} -o username={smb_user},password={smb_pass},uid={os.getuid()},gid={os.getgid()},forceuid,forcegid"
        )

        if os.path.isdir(path):
            shutil.copytree(
                path, f"{tmpdirname}/{destdirname}", copy_function=shutil.copy
            )
        else:
            print(f"Source directory {os.path.abspath(path)} is not a directory")
            exit(1)

        if json is not None:
            shutil.copy(path, f"{tmpdirname}/{destdirname}")

        print("Done!")
    except shutil.Error as e:
        print(f"Copy error: {e}")
        exit(1)
    except OSError as e:
        print(f"Copy error: {e}")
        exit(1)
    finally:
        os.system(f"sudo umount {tmpdirname}")

    exit(0)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Copy files to our network share")
    parser.add_argument(
        "path",
        action="store",
        nargs="?",
        type=str,
        help="optional path to the files directory",
    )
    parser.add_argument(
        "json",
        action="store",
        nargs="?",
        type=str,
        help="optional path to the json file",
    )

    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print("Keyboard interrupt, exiting")
