#!/usr/bin/env python3

import argparse
import json
import os
import random
from datetime import datetime
from os import environ as env
from typing import Optional

from dotenv import load_dotenv
from pytarallo import Tarallo
from pytarallo.Errors import NoInternetConnectionError
from rich import print
from rich.console import Console

from . import commons as peracommon


def main(the_args):
    load_dotenv()
    parsers = []

    if the_args.parsers is None:
        parsers = peracommon.ParserComponents.all()
    else:
        for parser_piece in the_args.parsers.split(","):
            try:
                parsers.append(peracommon.ParserComponents[parser_piece.strip()])
            except KeyError:
                print(f"[red]Unknown component parser: {parser_piece.strip()}[/]")
                print(f"Available parsers: " + ", ".join(peracommon.ParserComponents.all_keys()))
                exit(2)

    if the_args.path is None:
        generated_files_path = f"{os.getcwd()}/tmp"
    else:
        generated_files_path = the_args.path

    # if the_args.files is not None:
    #     peracommon.check_required_files(generated_files_path)

    # If we have to generate files...
    if not the_args.files:
        if os.path.isdir(generated_files_path):
            sel = input(f"Overwrite existing files in {generated_files_path} dir? y/N ").lower()
            if sel == "y":
                print("Overwriting...")
            else:
                sel = input("Output files to current working directory instead? y/N ").lower()
                if sel == "y":
                    generated_files_path = os.getcwd()
                    print("Outputting files to working directory...")
                else:
                    print("[blue]Quitting...[/]")
                    exit(-1)

        # if not generated_files_path:
        #     has_dependencies = peracommon.check_dependencies_for_generate_files()
        #     if not has_dependencies:
        #         if not ask_install_depdendencies():
        #             print("[blue]Quitting...[/]")
        #             exit(-1)

        # now that I have a dest folder, I generate files
        use_sudo = peracommon.env_to_bool(env.get("GENERATE_FILES_USE_SUDO", "1"))
        # ask_sudo_pass = peracommon.env_to_bool(env.get("GENERATE_FILES_ASK_SUDO_PASSWORD", "1"))
        try:
            generated_files_path = peracommon.generate_files(generated_files_path, use_sudo, None)
        except peracommon.GenerateFilesError as e:
            print(f"[red]Error: {str(e)}[/]")
            exit(2)

    gpu_location = get_gpu(the_args)

    # List of items only
    result = []
    try:
        result = peracommon.call_parsers(generated_files_path, set(parsers), gpu_location, True)
    except peracommon.InputFileNotFoundError as e:
        msg = f"[red]Cannot find required file: {e.path}[/]"
        if the_args.files:
            msg += "\nMake sure the file exists or selecting other parsers with -p"
        else:
            msg += "\nMake sure the file exists or try running generate_files.sh manually"
        exit(3)

    owner = get_owner()
    if owner:
        # List of items
        result = peracommon.add_owner(result, owner)

    # List of items and products
    result = peracommon.split_products(result)

    code = get_code()
    if code:
        # List of items
        found = peracommon.add_chassis_code(result, code)
        if not found:
            print("[red]Failed to add code to case! Maybe the case was not parsed?[/]")
            exit(1)

    # List of items as trees and products as products
    result = peracommon.make_tree(result)

    print_output(json.dumps(result, indent=2), generated_files_path)

    prompt_to_open_browser()

    upload_to_tarallo(result)


def ask_install_depdendencies():
    ans = input("You need to install some packages. Do you want to install them? y/N ").lower()
    if ans == "y":
        install_cmd = "apt install -y pciutils i2c-tools mesa-utils smartmontools dmidecode < /dev/null"
        if os.geteuid() != 0:
            os.system(f"sudo {install_cmd}")
        else:
            os.system(f"/bin/bash -c {install_cmd}")
        return True
    else:
        return False


def prompt_to_open_browser():
    import base64

    web_link = "aHR0cHM6Ly90YXJhbGxvLndlZWVvcGVuLml0L2J1bGsvYWRkCg=="
    web_link = base64.b64decode(web_link).decode("ascii").rstrip()
    egg = Console()
    text = [
        "Congratulations!!!",
        "You're",
        "the",
        "1000th",
        "WEEEisitor",
        "of",
        "the",
        "day",
    ]
    this_moment = datetime.now()
    if this_moment.minute == this_moment.second:
        for word in text:
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            egg.print(word, end=" ", style=f"rgb({red},{green},{blue})")
        egg.print(web_link)
    else:
        print(f"[green]Finished successfully![/] Now you can add this output to the T.A.R.A.L.L.O. -> {web_link}")


def upload_to_tarallo(data):
    msg_upload_ok = "[green]All went fine! [/] [blue]\nBye bye! [/]🍐\n"
    msg_upload_failed = "The upload failed. Check above and try to upload on your own"

    ans = input("Do you want to automatically upload the JSON to the T.A.R.A.L.L.O ? (Y/n): ").lower().rstrip()

    if ans.lower() == "n":
        print("\n[blue]Bye bye! [/]🍐\n")

        return

    try:
        t_url = env["TARALLO_URL"]
        t_token = env["TARALLO_TOKEN"]
    except KeyError:
        raise EnvironmentError("Missing definitions of TARALLO* environment variables (see the README)")

    while True:
        try:
            bulk_id = input("Please enter a bulk identifier (optional): ").rstrip()
            if bulk_id == "":
                bulk_id = None
            t = Tarallo.Tarallo(t_url, t_token)
            ver = t.bulk_add(data, bulk_id, False)
            if ver:
                print(msg_upload_ok)
                break
            else:
                overwrite = input("Cannot update, do you want to try overwriting the identifier? (y/N): ").lower().rstrip()
                if overwrite.lower() == "y":
                    ver = t.bulk_add(data, bulk_id, True)
                    if ver:
                        print(msg_upload_ok)
                        break
                    else:
                        print(msg_upload_failed)
                else:
                    bulk_id = input("Do you want to use another identifier? Just press enter for an automatic one. " "You choose (NEW_ID/n): ").rstrip()
                    if bulk_id.lower() != "n":
                        if bulk_id == "":
                            bulk_id = None
                        ver = t.bulk_add(data, bulk_id, True)
                        if ver:
                            print(msg_upload_ok)
                            break
                        else:
                            print(msg_upload_failed)

        except NoInternetConnectionError:
            print("\n[yellow]Unable to reach the T.A.R.A.L.L.O. " "Please connect this PC to the Internet and try again.[/]\n")


def get_gpu(the_args) -> peracommon.GpuLocation:
    # if the_args.files is not None:
    #     the_args.cpu = False
    #     the_args.gpu = False
    #     the_args.motherboard = False
    #
    #     try:
    #         with open(os.path.join(os.getcwd(), the_args.files, "gpu_location.txt")) as f:
    #             location = f.readline().lower().rstrip()
    #             if location == "mobo":
    #                 the_args.motherboard = True
    #             elif location == "gpu":
    #                 the_args.gpu = True
    #             elif location == "cpu":
    #                 the_args.cpu = True
    #     except FileNotFoundError:
    #         pass

    location = None
    if the_args.cpu:
        location = peracommon.GpuLocation.CPU
    elif the_args.gpu:
        location = peracommon.GpuLocation.DISCRETE
    elif the_args.motherboard:
        location = peracommon.GpuLocation.MOTHERBOARD
    elif the_args.gpu_none:
        location = peracommon.GpuLocation.NONE

    while not location:
        print(
            "\nWhere is GPU in your PC? c/g/b/n\n",
            "c for integrated in CPU\n",
            "g for discrete graphics card\n",
            "b for integrated in the motherboard\n",
            "n if there's none\n",
        )
        gpu_flag = input("Insert your choice: ").lower()
        if gpu_flag == "c":
            location = peracommon.GpuLocation.CPU
        elif gpu_flag == "g":
            location = peracommon.GpuLocation.DISCRETE
        elif gpu_flag == "b":
            location = peracommon.GpuLocation.MOTHERBOARD
        elif gpu_flag == "n":
            location = peracommon.GpuLocation.NONE
        else:
            location = None
    return location


def print_output(output: str, path: str):
    print("\nThe following output can be copy-pasted into the 'Bulk Add' page of the TARALLO, from '[' to ']':\n")
    print(output)

    with open(os.path.join(path, "copy_this_to_tarallo.json"), "w") as f:
        f.write(output)

    path = path.rstrip("/")
    print(
        f"You can also transfer the generated JSON file {path}/copy_this_to_tarallo.json to your PC with 'scp {path}/copy_this_to_tarallo.json <user>@<your_PC's_IP>:/path/on/your/PC' right from this terminal."
    )


def get_code() -> Optional[str]:
    if not args.code:
        code = input("Does this have a code already? (optional, ENTER to skip): ").strip()
    else:
        code = args.code
    if code and code != "":
        return code
    return None


def get_owner() -> Optional[str]:
    if not args.owner:
        owner = input("Do you want to add a owner? (optional, ENTER to skip): ").strip()
    else:
        owner = args.owner
    if owner and owner != "":
        return owner
    return None


def generate_parser():
    parser = argparse.ArgumentParser(
        description="Parse the files generated with generate_files.sh and " "get all the possible info out of them",
        epilog="If no argument is given, then this script will interactively guide you to run the PERACOTTA data gathering package."
        "Alternatively, you can choose to pass either the path to the directory where you want the files to be generated, the gpu location, or both."
        "In this case, the script will only become interactive when needed, and it won't ask you anything if you pass both the path and the gpu location.",
    )
    parser.add_argument(
        "-f",
        "--files",
        action="store_true",
        default=False,
        required=False,
        help="reuse previously generated files",
    )
    parser.add_argument(
        "--code",
        action="store",
        default=None,
        required=False,
        help="set the code assigned by T.A.R.A.L.L.O",
    )
    parser.add_argument("--owner", action="store", default=None, required=False, help="set a owner")
    parser.add_argument("-p", "--parsers", action="store", default=None, required=False, help="which parsers to use")
    gpu_group = parser.add_argument_group("GPU Location").add_mutually_exclusive_group(required=False)
    gpu_group.add_argument(
        "-g",
        "--gpu",
        action="store_true",
        default=False,
        help="computer has dedicated GPU",
    )
    gpu_group.add_argument(
        "-c",
        "--cpu",
        action="store_true",
        default=False,
        help="GPU is integrated inside the CPU",
    )
    gpu_group.add_argument(
        "-b",
        "--motherboard",
        action="store_true",
        default=False,
        help="GPU is integrated inside the motherboard",
    )
    gpu_group.add_argument(
        "--gpu-none",
        action="store_true",
        default=False,
        help="There's no GPU at all",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="print some warning messages",
    )
    parser.add_argument(
        "path",
        action="store",
        nargs="?",
        type=str,
        help="optional path where generated files are stored",
    )
    return parser


def __main():
    args = generate_parser().parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print("\n[blue]Quitting...[/]")


if __name__ == "__main__":
    __main()
