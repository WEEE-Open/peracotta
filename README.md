[![Python tests](https://github.com/WEEE-Open/peracotta/actions/workflows/python-tests.yml/badge.svg)](https://github.com/WEEE-Open/peracotta/actions/workflows/python-tests.yml)
[![Docker Image CI](https://github.com/WEEE-Open/peracotta/actions/workflows/docker-image.yml/badge.svg)](https://github.com/WEEE-Open/peracotta/actions/workflows/docker-image.yml)

# 🍐 P.E.R.A.C.O.T.T.A. 🍐

*Progetto Esteso Raccolta Automatica Configurazioni hardware Organizzate Tramite Tarallo Autonomamente*

Script to gather hardware data and update [T.A.R.A.L.L.O.](https://github.com/weee-open/tarallo) automatically.

## Common usage

You can have 2 use cases:
- a very old PC, that even struggles with showing the Desktop Environment
- a newer PC, which runs mostly fine even with graphical applications (like the DE, a browser, etc.)

In the first case, you want to use `main.py`. This is a CLI Python script that does almost everything the GUI does, which is almost as easy to use.  
In the second case, you want to use `main_with_gui.py`. This is the script which launches the GUI, and it's slightly easier to use than the CLI version.  

In both cases, please refer to the _How to run_ and _main.sh and main_with_gui.py_ sections.

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

If requirements change:  
- install the correct version of the requirements (e.g. a new library or a new version of an already installed library)  
- with the virtual environment activated, run `pip freeze > requirements-dev.txt` and *manually* edit the file (add the `-r requirements.txt` line and remove non-dev requirements)

## main.py and main_with_gui.py

These are the scripts you run directly from the terminal. Quite obviously, `main_with_gui.py` presents a graphical interface, and `main.py` runs in the terminal.

### main.py

This script basically runs `sudo ./generate_files.sh` and collect data into an appropriate json for T.A.R.A.L.L.O, but it does so in an interactive manner, so 
you can either pass it the arguments, or it will ask you for them nicely.

You can also pass as the -f/--files argument the directory where generate_files.sh dropped its files. By default (i.e. if you don't give any arguments 
to `generate_files.sh`) it will output the files in the current directory. Since this may clutter the working directory 
with txt files, it's best to make a new directory (e.g. `mkdir tmp`) and pass it to the file generator (e.g. `generate_files.sh tmp`).
You can then pass this path to this script so that it knows where to find the txt files (e.g. `./main.py -f tmp`).  
This is done automatically by the GUI version.


You can find the usage below, but keep in mind that the three most important arguments are:
- the path for files generation (if none given, it will default to a tmp directory, and if it exist, you will be asked whether you want to overwrite it).
- `-g | -c | -b`: one of these tells the script where the GPU (or graphics card if it's not integrated) is located. If none of them is given, a menu with the same choices will appear during the execution.
- the path to the txt files, previously generated with generate_files.sh.
```bash
usage: main.py [-h] [-f FILES] [-g | -c | -b] [-i] [-v] [path]

Parse the files generated with generate_files.sh and get all the possible info out of them

positional arguments:
  path                  optional path where generated files are stored

optional arguments:
  -h, --help            show this help message and exit
  -f FILES, --files FILES
                        retrieve previously generated files from a given path
  -v, --verbose         print some warning messages

GPU Location:
  -g, --gpu             computer has dedicated GPU
  -c, --cpu             GPU is integrated inside the CPU
  -b, --motherboard     GPU is integrated inside the motherboard

With or without GUI (one argument optional):
  -i, --gui             launch GUI instead of using the terminal version

```

### main_with_gui.py

This script is interactive, so you'll just need to run it with `./main_with_gui.py`. It does everything the terminal based version does, with the addition of a nice GUI.  
The GUI is also available from `main.py` with the `-i` or `--gui` option.

## Underlying scripts run by main.py and main_with_gui.py

### generate_files.sh

This will create some txt files with data related to the computer, that will be parsed by launching 
`main.py` with -f/--files argument. The hard work is powered by the many `read_X.py` scripts, which are the actual 
parsers.

Install dependencies on Debian-based distributions (Debian, Ubuntu, Xubuntu, etc):  
`sudo apt install pciutils i2c-tools mesa-utils smartmontools dmidecode`  
These are the actual programs that generate the files that we parse.

### parsers

There are many read_something.py scripts: these are used internally by the other scripts. They can also be launched from the command line. They can also be imported as libraries.

### data

This is the GUI icon.  
Yes, it's a pear emoji. 🍐
