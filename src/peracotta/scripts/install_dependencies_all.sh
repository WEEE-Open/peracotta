#!/bin/bash

CMD="apt install -y pciutils i2c-tools mesa-utils smartmontools dmidecode < /dev/null"

if [ "$EUID" -ne 0 ]; then
  sudo "$CMD"
else
  /bin/bash -c "$CMD"
fi
