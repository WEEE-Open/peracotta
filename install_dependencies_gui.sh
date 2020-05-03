#!/bin/bash

./install_dependencies_all.sh

sudo apt install python3-pip python3-venv
if [ ! -d venv ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt

# remember to `deactivate` to exit the venv