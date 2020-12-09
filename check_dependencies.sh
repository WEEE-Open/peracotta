#!/bin/bash

if ! command -v pciutils i2c-tools mesa-utils smartmontools dmidecode >/dev/null 2>&1; then
  exit 1
else
  exit 0
fi
