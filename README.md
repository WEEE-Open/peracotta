# P.E.R.A.C.O.T.T.A.

*Progetto Esteso Raccolta Automatica Configurazioni hardware Organizzate Tramite Tarallo Autonomamente*

Script to gather hardware data and update [T.A.R.A.L.L.O.](weee-open/tarallo) automatically.

Use `pipenv shell` to get a virtual environment and run the scripts.

## generate_files.sh

This will create some txt files with data related to the computer.

## extract_data.py

Point it to the directory where generate_files.sh dropped its files

```
usage: extract_data.py [-h] [-s] [-g] [-c] [-i] [path]

Get all the possible output data things

positional arguments:
  path               to directory with txt files

optional arguments:
  -h, --help         show this help message and exit
  -s, --short        print shorter ouput
  -g, --gpu          computer has dedicated GPU
  -c, --cpu          integrated GPU is inside CPU (default to mobo)
  -i, --interactive  print some warning messages
```

## main_with_gui.py

Launch it, there's a GUI. It looks cool.

## read_X.py

There are many read_something.py scripts: these are used internally by the other scripts. They can also be launched from the command line. They can also be imported as libraries.
