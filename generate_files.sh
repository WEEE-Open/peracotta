#!/usr/bin/env bash

dmidecode -t baseboard > $1/baseboard.txt
dmidecode -t connector > $1/connector.txt
dmidecode -t chassis > $1/chassis.txt
lscpu > $1/lscpu.txt
lspci -v > $1/lspci.txt
glxinfo > $1/glxinfo.txt
DISKZ=($(lsblk -d -I 8 -o NAME -n))
echo Found ${#DISKZ[@]} disks
for d in "${DISKZ[@]}"
do
	smartctl -x /dev/$d > $1/smartctl-dev-$d.txt
done
# Already done on our custom distro, but repetita iuvant
modprobe at24
modprobe eeprom
decode-dimms > $1/dimms.txt
