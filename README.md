# P.E.R.A.C.O.T.T.A.

*Progetto Esteso Raccolta Automatica Configurazioni hardware Organizzate Tramite Tarallo Autonomamente*

Script to gather hardware data and update [T.A.R.A.L.L.O.](weee-open/tarallo) automatically.

## Common usage

You can have 2 use cases:
- a very old PC, that even struggles with showing the Desktop Environment
- a newer PC, which runs mostly fine even with graphical applications (like the DE, a browser, etc.)

In the first case, you want to use `main.sh`. This is a CLI Bash script that does almost everything the GUI does, which is almost as easy to use.  
In the second case, you want to use `main_with_gui.py`. This is the script which launches the GUI, and it's slightly easier to use than the CLI version.  

In both cases, please refer to the _How to run_ and _main.sh and main_with_gui.py_ sections.

## How to run

Clone this repo:  
`git clone https://github.com/weee-open/peracotta`  
Make a virtual environment in the directory of the repo:  
`cd peracotta`    

If you want to use the GUI, the following additional steps are needed:  
`python3 -m venv venv`  
Activate it:  
`source venv/bin/activate`  
Install the requirements in the virtual environment:  
`pip install -r requirements.txt`  
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

## main.sh and main_with_gui.py

These are the scripts you run directly from the terminal. Quite obviously, `main_with_gui.py` presents a graphical interface, and `main.sh` runs in the terminal.

### main.sh

This script basically runs `sudo ./generate_files.sh` and `./extract_data.py`, but it does so in an interactive manner, so 
you can either pass it the arguments, or it will ask you for them nicely.

```
Use -h or --help to show this help.
Usage (either the first line or the second one):
./main.sh -f|--files <optional path where previously generated files are stored>
./main.sh [-p|--path <optional path to generate files to>] [-c|--cpu | -g|--gpu | -b|--motherboard]

If no argument is given, then this script will interactively guide you to run the PERACOTTA data gathering package.
Alternatively, you can choose to pass either the path to the directory where you want the files to be generated, the gpu location, or both.
In this case, the script will only become interactive when needed, and it won't ask you anything if you pass both the path and the gpu location.

When using -f or --files, this script will skip the generation step and it will print out the content of previously generated files, if all required files are found in the given directory (tmp by default).

```
### main_with_gui.py

This script is interactive, so you'll just need to run it with `./main_with_gui.py`. It does everything the terminal based version does, with the addition of a nice GUI.  
The GUI is also available from `extract_data.py` with the `-i` or `--gui` option.

## Underlying scripts run by main.sh and main_with_gui.py

### generate_files.sh

This will create some txt files with data related to the computer, that will be parsed by launching 
`extract_data.py`. The hard work is powered by the many `read_X.py` scripts, which are the actual 
parsers.

Install dependencies on Debian-based distributions (Debian, Ubuntu, Xubuntu, etc):  
`sudo apt install pciutils i2c-tools mesa-utils smartmontools dmidecode`  
These are the actual programs that generate the files that we parse.

### extract_data.py

#### Note: You can run this script after running `sudo ./generate_files.sh`, but it's quicker and easier if you just run `./main.sh`. No `sudo` required.

You can pass as the path argument the directory where generate_files.sh dropped its files. By default (i.e. if you don't give any arguments 
to `generate_files.sh`) it will output the files in the current directory. Since this may clutter the working directory 
with txt files, it's best to make a new directory (e.g. `mkdir tmp`) and pass it to the file generator (e.g. `generate_files.sh tmp`).
You can then pass this path to this script so that it knows where to find the txt files (e.g. `./extract_data.py -g tmp`).  
This is done automatically by the GUI version.  
  
You can find the usage below, but keep in mind that the two most important arguments are:
- the path to the txt files (if none given, it will default to the current directory)
- `-g | -c | -b`: one of these is required to tell the script where the GPU (or graphics card if it's not integrated) is located

```
usage: extract_data.py [-h] (-g | -c | -b) [-s | -l | -i] [-v] [path]

Parse the files generated with generate_files.sh and get all the possible info
out of them

positional arguments:
  path               path to directory with txt files generated by
                     generate_files.sh - defaults to current directory

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      print some warning messages

GPU Location (one argument required):
  -g, --gpu          computer has dedicated GPU
  -c, --cpu          GPU is integrated inside the CPU
  -b, --motherboard  GPU is integrated inside the motherboard

With or without GUI (one argument optional):
  -s, --short        enabled by default, this is the option you want if you
                     want to copy-paste this output into the TARALLO 'Bulk
                     Add' page
  -l, --long         print longer output
  -i, --gui          launch GUI instead of using the terminal version
```

### parsers

There are many read_something.py scripts: these are used internally by the other scripts. They can also be launched from the command line. They can also be imported as libraries.

### data

This is the GUI icon.  
Yes, it's a pear emoji. 🍐
