#!/usr/bin/env bash

dmidecode -t baseboard >> baseboard.txt
dmidecode -t chassis >> chassis.txt
lscpu >> lscpu.txt
lspci -v >> lspci.txt
smartctl -x /dev/sda >> smartctl.txt
# Already done on our custom distro, but repetita iuvant
modprobe at24
modprobe eeprom
decode-dimms >> dimms.txt
