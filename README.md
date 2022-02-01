[![Python Tests](https://github.com/WEEE-Open/peracotta/actions/workflows/python-tests.yml/badge.svg)](https://github.com/WEEE-Open/peracotta/actions/workflows/python-tests.yml)
[![Docker Image CI](https://github.com/WEEE-Open/peracotta/actions/workflows/docker-image.yml/badge.svg)](https://github.com/WEEE-Open/peracotta/actions/workflows/docker-image.yml)
[![Linting](https://github.com/WEEE-Open/peracotta/actions/workflows/lint.yml/badge.svg)](https://github.com/WEEE-Open/peracotta/actions/workflows/lint.yml)

# 🍐 P.E.R.A.C.O.T.T.A. 🍐

*Progetto Esteso Raccolta Automatica Configurazioni hardware Organizzate Tramite Tarallo Autonomamente*

Script to gather hardware data and update [T.A.R.A.L.L.O.](https://github.com/weee-open/tarallo) automatically.

## Common usage

You can have 2 use cases:
- a very old PC, that even struggles with showing the Desktop Environment
- a newer PC, which runs mostly fine even with graphical applications (like the DE, a browser, etc.)

In the first case, you want to use `peracruda`. This is a CLI Python script that does almost everything the GUI does, which is almost as easy to use.  
In the second case, you want to use `peracotta`. This is the script which launches the GUI, and it's slightly easier to use than the CLI version.  

In both cases, please refer to the _How to run_ and _main.sh and peracotta_ sections.

## How to run

Clone this repo:  
`git clone https://github.com/weee-open/peracotta`  
Make a virtual environment in the directory of the repo:  
`cd peracotta`    
`python3 -m venv venv`  
Activate it:  
`source venv/bin/activate`  
Install the requirements in the virtual environment:  
`pip install -r requirements.txt`  
Copy and modify to your needs the .env example file into the actual .env:  
`cp .env.example .env`  
Use it.  
When you're done, exit the virtualenv with `deactivate` 
or simply close the terminal you were using.

### How to develop

Same as before, until the `pip install` part. The correct command is:    
`pip install -r requirements-dev.txt`  

This will allow you to run tests: `pytest -vv tests`

Some markers are also available, e.g. you can run `pytest -m gui` to just test the gui, or `pytest -m 'not gui'` to test everything else. See `pytest.ini` for a list of markers.

If requirements change:  
- install the correct version of the requirements (e.g. a new library or a new version of an already installed library)  
- with the virtual environment activated, run `pip freeze > requirements-dev.txt` and *manually* edit the file (add the `-r requirements.txt` line and remove non-dev requirements)

If you can't generate the files because you don't have access to `sudo`, such as on our development VM, you should use the files in a directory from `tests`.

## peracotta and peracruda

These are the scripts you run directly from the terminal. Quite obviously, `peracotta` presents a graphical interface, and `peracruda` runs in the terminal.

### peracruda (CLI)

This script basically runs `sudo ./generate_files.sh` and collect data into an appropriate json for T.A.R.A.L.L.O, but it does so in an interactive manner, so 
you can either pass it the arguments, or it will ask you for them nicely.

You can also pass as the -f/--files argument the directory where generate_files.sh dropped its files. By default (i.e. if you don't give any arguments 
to `generate_files.sh`) it will output the files in the current directory. Since this may clutter the working directory 
with txt files, it's best to make a new directory (e.g. `mkdir tmp`) and pass it to the file generator (e.g. `generate_files.sh tmp`).
You can then pass this path to this script so that it knows where to find the txt files (e.g. `./peracruda -f tmp`).  
This is done automatically by the GUI version.


You can find the usage below, but keep in mind that the three most important arguments are:
- the path for files generation (if none given, it will default to a tmp directory, and if it exist, you will be asked whether you want to overwrite it).
- `-g | -c | -b`: one of these tells the script where the GPU (or graphics card if it's not integrated) is located. If none of them is given, a menu with the same choices will appear during the execution.
- `--code CODE` and `--owner OWNER`: these two parameters are used to add some more information directly into the output json file. 
- the path to the txt files, previously generated with generate_files.sh.

```
usage: peracotta-cli [-h] [-f] [--code CODE] [--owner OWNER]
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

This script is interactive, so you'll just need to run it with `./peracotta`. It does everything the terminal based version does, with the addition of a nice GUI.

## Underlying scripts run by peracotta and peracruda

### generate_files.sh

This will create some txt files with data related to the computer, that will be parsed by launching 
`peracruda` with -f/--files argument. The hard work is powered by the many `read_X.py` scripts, which are the actual 
parsers.

Install dependencies on Debian-based distributions (Debian, Ubuntu, Xubuntu, etc):  
`sudo apt install pciutils i2c-tools mesa-utils smartmontools dmidecode`  
These are the actual programs that generate the files that we parse.

### parsers

There are many read_something.py scripts: these are used internally by the other scripts.
They can also be launched from the command line.
They can also be imported as libraries.

### data

This is the GUI icon.  
Yes, it's a pear emoji. 🍐

Fan icons created by <a href="https://www.flaticon.com/free-icons/fan" title="fan icons">juicy_fish</a> - Flaticon