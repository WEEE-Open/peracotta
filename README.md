# P.E.R.A.C.O.T.T.A.

*Progetto Esteso Raccolta Automatica Configurazioni hardware Organizzate Tramite Tarallo Autonomamente*

Script to gather hardware data and update [T.A.R.A.L.L.O.](weee-open/tarallo) automatically.

Use `pipenv shell` to get a virtual environment and run the scripts.

## generate_files.sh

This will create some txt files with data related to the computer, that will be parsed by launching 
`extract_data.py`. The hard work is powered by the many `read_X.py` scripts, which are the actual 
parsers.

## extract_data.py

Point it to the directory where generate_files.sh dropped its files

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

## main_with_gui.py

Launch it, there's a GUI. It looks cool.  
The GUI is also available from `extract_data.py` with the `-i` or `--gui` option.

## read_X.py

There are many read_something.py scripts: these are used internally by the other scripts. They can also be launched from the command line. They can also be imported as libraries.
