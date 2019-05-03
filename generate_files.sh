#!/usr/bin/bash

if [ $# -eq 0 ]; then
    echo "No path given: outputting files in working directory"
    OUTPATH="."
elif [ $# -eq 1 ]; then
    echo "Outputting files to "$1
    OUTPATH=$1
else
    echo "Unexpected number of parameters. Usage: sudo ./generate_files.sh /optional/path/to/files"
fi

dmidecode -t baseboard > $OUTPATH/baseboard.txt
dmidecode -t connector > $OUTPATH/connector.txt
dmidecode -t chassis > $OUTPATH/chassis.txt
lscpu > $OUTPATH/lscpu.txt
lspci -v > $OUTPATH/lspci.txt
glxinfo > $OUTPATH/glxinfo.txt
DISKZ=($(lsblk -d -I 8 -o NAME -n))
echo Found ${#DISKZ[@]} disks
for d in "${DISKZ[@]}"
do
	smartctl -x /dev/$d > $OUTPATH/smartctl-dev-$d.txt
done
# Already done on our custom distro, but repetita iuvant
modprobe at24
modprobe eeprom
decode-dimms > $OUTPATH/dimms.txt
