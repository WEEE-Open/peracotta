#!/bin/bash

dpkg -s pciutils i2c-tools mesa-utils smartmontools dmidecode &> /dev/null

if [ $? -eq 0 ]; then
  exit 0
else
  exit 1
fi