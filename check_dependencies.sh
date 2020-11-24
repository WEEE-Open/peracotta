#!/bin/bash
if ! command -v pciutils i2c-tools mesa-utils smartmontools dmidecode >/dev/null 2>&1; then
  return 1
else
  return 0
fi