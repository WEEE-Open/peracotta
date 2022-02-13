[![Python Tests](https://github.com/WEEE-Open/peracotta/actions/workflows/python-tests.yml/badge.svg)](https://github.com/WEEE-Open/peracotta/actions/workflows/python-tests.yml)
[![Docker Image CI](https://github.com/WEEE-Open/peracotta/actions/workflows/docker-image.yml/badge.svg)](https://github.com/WEEE-Open/peracotta/actions/workflows/docker-image.yml)
[![Linting](https://github.com/WEEE-Open/peracotta/actions/workflows/lint.yml/badge.svg)](https://github.com/WEEE-Open/peracotta/actions/workflows/lint.yml)

# 🍐 P.E.R.A.C.O.T.T.A. 🍐

*Progetto Esteso Raccolta Automatica Configurazioni hardware Organizzate Tramite Tarallo Autonomamente*

Program to gather data, display it and update [T.A.R.A.L.L.O.](https://github.com/weee-open/tarallo) automatically.

## Common usage

Multiple use cases are possible. More details on each program are provided in the *How to install and run* section.

### You are using a relatively fast pc

Launch `peracotta`: that is the GUI that allows you to gather data, parse it and display it.

![Main peracotta window, displaying a motherboard](/S/Software/peracotta/docs/peracotta_mobo_screenshot.png)

Options can be configured in the left pane, then after Generate is pressed data is displayed in the right pane.  
Some basic editing is possible (add and remove items and features, edit feature values). The result can be saved as a JSON or uploaded directly to tarallo.

### You are using a slow pc or you don't have PyQt installed

Launch `peracruda` from the terminal: this a script that gathers and parses data, however it offers no editing capabilities.  
At the end, you can save data as a JSON or upload it to tarallo directly.

The saved JSON can be uploaded to tarallo or imported from the `peracotta` GUI e.g. on another computer, to review and edit it before upload.

### You are on a pc that barely runs

If you are desperate and the entire system is unstable due to failing hardware or any other reason, run `scripts/generate_files.sh`. That's the most bare-bones way to gather data: the script takes a single (optional) parameter for the output directory, and generates some txt files. No parsing is done.

You can load those files in `peracruda` (`-f` option) or `peracotta` (`File > Load raw files` option) and continue from there.

## How to install and run

```bash
# Clone this repo
git clone https://github.com/weee-open/peracotta

# Make a virtual environment and activate it
cd peracotta
python3 -m venv venv
source venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# Copy the example .env file and edit it to your liking
cp .env.example .env
nano .env
```

### How to develop

Same as before, until the `pip install` part. Just install `requirements-dev.txt` instead:
`pip install -r requirements-dev.txt`  

This will allow you to run tests: `pytest -vv tests`

Some markers are also available, e.g. you can run `pytest -m gui` to just test the gui, or `pytest -m 'not gui'` to test everything else. See `pytest.ini` for a list of markers.

If requirements change:  
- install the correct version of the requirements (e.g. a new library or a new version of an already installed library)  
- with the virtual environment activated, run `pip freeze > requirements-dev.txt` and *manually* edit the file (add the `-r requirements.txt` line and remove non-dev requirements)

If you can't run generate_files.sh because you don't have access to `sudo`, such as on our development VM, you can look at `tests/source_files` for examples.

### peracruda (CLI)

This script basically runs `sudo ./generate_files.sh` and collect data into an appropriate json for T.A.R.A.L.L.O, but it does so in an interactive manner, so you can either pass it the arguments, or it will ask you for them nicely.

You can also pass as the -f/--files argument the directory where generate_files.sh dropped its files.

You can find the usage below, but keep in mind that the three most important arguments are:

- the path for files generation: if none given, it will default to a tmp directory, and if it exists, you will be asked whether you want to overwrite it
- `-g | -c | -b`: one of these tells the script where the GPU (or graphics card if it's not integrated) is located. If none of them is given, a menu with the same choices will appear during the execution.
- `--code CODE` and `--owner OWNER`: these two parameters are used to add some more information directly into the output json file. 
- `-f` to read files from the path instead of calling `generate_files.sh` again.

```
usage: peracruda [-h] [-f] [--code CODE] [--owner OWNER]
                 [-g | -c | -b | --gpu-none] [-v]
                 [path]
Parse the files generated with generate_files.sh and get all the possible info
out of them
positional arguments:
  path               optional path where generated files are stored
optional arguments:
  -h, --help         show this help message and exit
  -f, --files        reuse previously generated files
  --code CODE        set the code assigned by T.A.R.A.L.L.O
  --owner OWNER      set a owner
  -v, --verbose      print some warning messages
GPU Location:
  -g, --gpu          computer has dedicated GPU
  -c, --cpu          GPU is integrated inside the CPU
  -b, --motherboard  GPU is integrated inside the motherboard
  --gpu-none         There's no GPU at all
```

### peracotta (GUI)

Just need to run it with `./peracotta` or from your file manager. It does everything the terminal based version does and more, all through a GUI.

### generate_files.sh

This will create some txt files with data related to the computer, that will be parsed by launching 
`peracruda` with -f/--files argument. The hard work is powered by the many `read_X.py` scripts, which are the actual 
parsers.

Install dependencies on Debian-based distributions (Debian, Ubuntu, Xubuntu, etc):  
`sudo apt install pciutils i2c-tools mesa-utils smartmontools dmidecode`  
These are the actual programs that generate the files that we parse.

### parsers

There are many read_something.py scripts in the `parsers` directory: these are used internally by the other scripts.
They can also be launched from the command line, with very basic parameters.
They can also be imported as libraries.

### assets

This directory contains some images and other files used by the GUI.  
Fan icons created by <a href="https://www.flaticon.com/free-icons/fan" title="fan icons">juicy_fish</a> - Flaticon
